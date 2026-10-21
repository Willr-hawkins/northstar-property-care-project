from django.conf import settings
from django.db import models, transaction

from core.models import TimeStampModel

FORMER_STAFF_LABEL = "Former staff member"

def staff_display_name(user):
    """
    Name shown for a staff member on notes and the activity timeline.
    Current staff: full name if set, else username.
    Deactivated or deleted staff: 'Former staff member'.
    """
    if user is None or not user.is_active:
        return FORMER_STAFF_LABEL
    return user.get_full_name() or user.get_username()

class Enquiry(TimeStampModel):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        QUOTED = "quoted", "Quoted"
        WON = "won", "Won"
        LOST = "lost", "Lost"

    class ContactMethod(models.TextChoices):
        EMAIL = "email", "Email"
        PHONE = "phone", "Phone"

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    service = models.ForeignKey(
        "services.Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="enquiries",
    )
    postcode = models.CharField(max_length=10)
    project_description = models.TextField()
    preffered_contact_method = models.CharField(
        max_length=10, choices=ContactMethod.choices, blank=True
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "enquiries"
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["-created_at"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(status__in=["new", "contacted", "quoted", "won", "lost"]),
                name="enquiry_status_valid",
            ),
        ]

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
    
    def change_status(self, new_status, user):
        """
        Move the enquiry to a new status and record the change.

        Returns True if the status changed, False if it was already that status.
        Raised ValueError for a status that isn't one of Enquiry.Status.
        """
        if new_status not in self.Status.values:
            raise ValueError(f"Invalid status: {self.status!r}")
        if new_status == self.status:
            return False
        
        with transaction.atomic():
            old_status = self.status
            self.status = new_status
            self.save(update_fields=["status", "updated_at"])
            EnquiryStatusChange.objects.create(
                enquiry=self,
                from_status=old_status,
                to_status=new_status,
                changed_by=user,
            )
        return True
    

class EnquiryNote(TimeStampModel):
    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name="notes")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="enquiry_notes",
    )
    body = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Note on {self.enquiry.name} by {self.author_display_name}"
        
    @property
    def author_display_name(self):
        return staff_display_name(self.author)
    
    @property
    def author_is_former_staff(self):
        return self.author is None or not self.author.is_active
    

class EnquiryStatusChange(models.Model):
    """ One row per status change - powers the enquiry activity timeline. """

    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name="status_changes")
    from_status = models.CharField(max_length=20, choices=Enquiry.Status.choices)
    to_status = models.CharField(max_length=20, choices=Enquiry.Status.choices)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="enquiry_status_changes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
    
    def __str__(self):
        return f"{self.enquiry.name}: {self.from_status} → {self.to_status}"
    
    @property
    def changed_by_display_name(self):
        return staff_display_name(self.changed_by)
    
    @property
    def changed_by_is_former_staff(self):
        return self.changed_by is None or not self.changed_by.is_active

