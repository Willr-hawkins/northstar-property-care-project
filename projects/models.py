from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.models import TimeStampModel

class ProjectQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)
    
    def featured(self):
        return self.published().filter(is_featured=True)
    
class Project(TimeStampModel):
    class Category(models.TextChoices):
        RENOVATION = "renovation", "Renovation"
        KITCHEN = "kitchen", "Kitchen"
        BATHROOM = "bathroom", "Bathroom"
        EXTENSION = "extension", "Extension"
        MAINTENANCE = "maintenance", "Maintenance"

    title = models.CharField(max_length=120)
    slug = models.CharField(max_length=140, unique=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    service = models.ForeignKey(
        "services.Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
        help_text="Optional - links this project to a service page as related work.",
    )
    summary = models.CharField(max_length=200, help_text="Short line shown under the project card.")
    description = models.TextField()
    featured_image = models.ImageField(upload_to="projects/featured/")
    featured_image_alt = models.CharField(max_length=200)
    location = models.CharField(max_length=80, blank=True)
    is_featured = models.BooleanField(default=False, help_text="Show on the homepage.")
    is_published = models.BooleanField(
        default=False, help_text="Only published projects appear on the public site."
    )
    completed_at = models.DateField(null=True, blank=True)

    objects = ProjectQuerySet.as_manager()

    class Meta:
        ordering = ["-completed_at", "-created_at"]
        indexes = [
            models.Index(fields=["is_published", "category"]),
            models.Index(fields=["is_published", "is_featured"]),
        ]

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"slug": self.slug})
    

class ProjectImage(TimeStampModel):
    class Kind(models.TextChoices):
        GALLERY = "gallery", "Gallery"
        BEFORE = "before", "Before"
        AFTER = "after", "After"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/gallery/")
    alt_text = models.CharField(max_length=200)
    caption = models.CharField(max_length=200, blank=True)
    kind = models.CharField(max_length=10, choices=Kind.choices, default=Kind.GALLERY)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"{self.project.title} - {self.get_kind_display()} #{self.display_order}"