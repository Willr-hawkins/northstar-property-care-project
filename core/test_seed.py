import pytest
from django.core.management import CommandError, call_command
from PIL import Image

from core import seed_data
from core.management.commands.seed_demo import required_image_stems
from enquiries.models import Enquiry, EnquiryNote
from projects.models import Project, ProjectImage
from services.models import Service

pytestmark = pytest.mark.django_db


@pytest.fixture
def seed_images(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path / "media"  # keep test uploads out of your real media folder
    images_dir = tmp_path / "images"
    images_dir.mkdir()
    for stem in required_image_stems():
        Image.new("RGB", (10, 10), "white").save(images_dir / f"{stem}.jpg")
    return images_dir


def run_seed(images_dir):
    call_command("seed_demo", images_dir=str(images_dir), stdout=open("/dev/null", "w"))


def test_seed_created_demo_content(seed_images):
    run_seed(seed_images)
    assert Service.objects.count() == len(seed_data.SERVICES)
    assert Project.objects.count() == len(seed_data.PROJECTS)
    assert Project.objects.published().count() == sum(p["is_published"] for p in seed_data.PROJECTS)
    assert Enquiry.objects.count() == len(seed_data.ENQUIRIES)


def test_seed_is_safe_to_run_twice(seed_images):
    run_seed(seed_images)
    run_seed(seed_images)
    assert Service.objects.count() == len(seed_data.SERVICES)
    assert Project.objects.count() == len(seed_data.PROJECTS)
    assert ProjectImage.objects.count() == 4
    assert Enquiry.objects.count() == len(seed_data.ENQUIRIES)


def test_seed_never_deletes_real_enquiries(seed_images):
    real = Enquiry.objects.create(
        name="Real Customer", email="customer@realdomain.co.uk",
        postcode="BS1 1AA", project_description="A genuine enquiry.",
    )
    run_seed(seed_images)
    assert Enquiry.objects.filter(pk=real.pk).exists()


def test_seed_includes_current_and_former_staff_notes(seed_images):
    run_seed(seed_images)
    notes = list(EnquiryNote.objects.select_related("author"))
    assert any(n.author_is_former_staff for n in notes)
    assert any(not n.author_is_former_staff for n in notes)


def test_seed_fails_clearly_when_images_missing(tmp_path):
    with pytest.raises(CommandError, match="Missing seed images"):
        call_command("seed_demo", images_dir=str(tmp_path))