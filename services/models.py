from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.models import TimeStampModel

class ServiceQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
    
class Service(TimeStampModel):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    short_description = models.CharField(
        max_length=200, help_text="One or two sentences for the service list and cards."
    )
    description = models.TextField(help_text="Full description for the service detail page.")
    image = models.ImageField(upload_to="services/")
    image_alt = models.CharField(
        max_length=200, help_text="Describe the photo for the screen-reader users."
    )
    is_active = models.BooleanField(
        default=True, help_text="Untick to hide this service from the public site."
    )
    display_order = models.PositiveSmallIntegerField(
        default=0, help_text="Lower numbers appear first."
    )

    objects = ServiceQuerySet.as_manager()

    class Meta:
        ordering = ["display_order", "title"]
        indexes = [models.Index(fields=["is_active", "display_order"])]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("services:detail", kwargs={"slug": self.slug})
