import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Enquiry

logger = logging.getLogger(__name__)


def send_enquiry_notification(enquiry, amdin_url=""):
    """
    Email the team about a new enquiry and record whether it was sent.

    Never raises: the enquiry is already saved, so a mail failure is logged
    and stored on the enquiry instead of reaching the customer.
    Returns True if the email was handed to the mail server.
    """
    context = {"enquiry": enquiry, "admin_url": amdin_url}
    service = enquiry.service.title if enquiry.service else "Not sure yet"

    message = EmailMultiAlternatives(
        subject=f"New enquiry: {enquiry.name} - {service}",
        body=render_to_string("enquiries/email/new_enquiry.txt", context),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.ENQUIRY_NOTIFICATION_EMAIL],
        reply_to=[enquiry.email],
    )
    message.attach_alternative(render_to_string("enquiries/email/new_enquiry.html", context), "text/html")

    try:
        message.send()
    except Exception as error:   # SMTP errors, timeouts, bad credentials ....
        logger.exception("Enquiry %s notification email failed.", enquiry.pk)
        Enquiry.objects.filter(pk=enquiry.pk).update(
            notification_status=Enquiry.NotificationStatus.FAILED,
            notification_error=f"{type(error).__name__}: {error}"[:500],
        )
        return False
    
    Enquiry.objects.filter(pk=enquiry.pk).update(
        notification_status=Enquiry.NotificationStatus.SENT,
        notification_error="",
    )
    return True