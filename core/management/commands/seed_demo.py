from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from core import seed_data
from enquiries.models import Enquiry, EnquiryNote, EnquiryStatusChange
from projects.models import Project, ProjectImage
from services.models import Service

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")
DEMO_EMAIL_SUFFIX = "@example.com"


def required_image_stems():
    """ Every image file name (without extension) the seed date refers to. """
    stems = [s["image"] for s in seed_data.SERVICES]
    for project in seed_data.PROJECTS:
        stems.append(project["image"])
        stems.extend(g["image"] for g in project.get("gallery", []))
    return stems


class Command(BaseCommand):
    help = "Load demo services, projects, staff and enquiries. Safe to run repeatedly."

    def add_arguments(self, parser):
        parser.add_argument(
            "--images-dir",
            default=str(settings.BASE_DIR / "seed" / "images"),
            help="Folder containing the seed photographs.",
        )
    
    def handle(self, *args, **options):
        self.images_dir = Path(options["images_dir"])
        self.check_images()

        with transaction.atomic():
            services = self.seed_services()
            self.seed_projects(services)
            staff = self.seed_staff()
            self.seed_enquiries(services, staff)

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Service.objects.count()} services, "
            f"{Project.objects.count()} projects ({Project.objects.published().count()} published), "
            f"{ProjectImage.objects.count()} project images, "
            f"{Enquiry.objects.filter(email__endswith=DEMO_EMAIL_SUFFIX).count()} demo enquiries."
        ))

    # --- Images -------------------------------------------------------------

    def find_image(self, stem):
        for extension in IMAGE_EXTENSIONS:
            path = self.images_dir / f"{stem}{extension}"
            if path.exists():
                return path
        return None
    
    def check_images(self):
        missing = [stem for stem in required_image_stems() if self.find_image(stem) is None]
        if missing:
            raise CommandError(
                f"Missing seed images in {self.images_dir}:\n  " + "\n ".join(missing)
            )
        
    def attach_image(self, field_file, stem):
        path = self.find_image(stem)
        with path.open("rb") as handle:
            field_file.save(path.name, File(handle), save=False)

    # --- Content -----------------------------------------------------

    def seed_services(self):
        services = {}
        for data in seed_data.SERVICES:
            data = dict(data)
            slug, stem = data.pop("slug"), data.pop("image")
            service, _ = Service.objects.update_or_create(slug=slug, defaults=data)
            if not service.image:
                self.attach_image(service.image, stem)
                service.save()
            services[slug] = service
        return services
    
    def seed_projects(self, services):
        for data in seed_data.PROJECTS:
            data = dict(data)
            slug, stem = data.pop("slug"), data.pop("image")
            gallery = data.pop("gallery", [])
            data["service"] = services.get(data.pop("service"))

            project, _ = Project.objects.update_or_create(slug=slug, defaults=data)
            if not project.featured_image:
                self.attach_image(project.featured_image, stem)
                project.save()

            if not project.images.exists():
                for order, image_data in enumerate(gallery, start=1):
                    image = ProjectImage(
                        project=project,
                        kind=image_data["kind"],
                        alt_text=image_data["alt_text"],
                        caption=image_data.get("caption", ""),
                        display_order=order,
                    )
                    self.attach_image(image.image, image_data["image"])
                    image.save()

    
    def seed_staff(self):
        User = get_user_model()
        staff = {}
        for data in seed_data.STAFF:
            data = dict(data)
            username = data.pop("username")
            user, created = User.objects.update_or_create(
                username=username, defaults={**data, "is_staff": True}
            )
            if created:
                user.set_unusable_password()
                user.save()
            staff[username] = user
        return staff
    
    def seed_enquiries(self, services, staff):
        # Only demo enquiries are replaced: real form submissions are never touched.
        Enquiry.objects.filter(email__endswith=DEMO_EMAIL_SUFFIX).delete()
        now = timezone.now()

        for data in seed_data.ENQUIRIES:
            data = dict(data)
            days_ago = data.pop("days_ago")
            history = data.pop("history", [])
            notes = data.pop("notes", [])
            data["service"] = services.get(data.pop("service"))

            enquiry = Enquiry.objects.create(**data)

            for new_status, username, change_days_ago in history:
                enquiry.change_status(new_status, staff[username])
                change = enquiry.status_changes.order_by("-pk").first()
                EnquiryStatusChange.objects.filter(pk=change.pk).update(
                    created_at=now - timedelta(days=change_days_ago)
                )

            for username, body, note_days_ago in notes:
                note = EnquiryNote.objects.create(
                    enquiry=enquiry, author=staff[username], body=body
                )
                stamp = now - timedelta(days=note_days_ago)
                EnquiryNote.objects.filter(pk=note.pk).update(created_at=stamp, updated_at=stamp)

            activity = [days_ago] + [h[2] for h in history] + [n[2] for n in notes]
            Enquiry.objects.filter(pk=enquiry.pk).update(
                created_at=now - timedelta(days=days_ago),
                updated_at=now - timedelta(days=min(activity)),
            )