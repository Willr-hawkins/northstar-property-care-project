from django.db import models

class TimeStampModel(models.Model):
    """ Abstract base: adds created/updated timestamps to any model that inherits it. """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
