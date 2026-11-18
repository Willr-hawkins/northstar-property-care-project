from smtplib import SMTPException

import pytest
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse

from enquiries.models import Enquiry
from enquiries.notifications import send_enquiry_notification

pytestmark = pytest.mark.django_db

QUOTE_URL = reverse("enquiries:quote")


def make_enquiry(**kwargs):
    defaults = {
        "name": "Hannah Clarke",
        "email": "hannah@example.com",
        "postcode": "BS8 1AA",
        "project_description": "New kitchen and knock through to the dining room.",
    }
    defaults.update(kwargs)
    return Enquiry.objects.create(**defaults)


def valid_post(**overrides):
    data = {
        "name": "Hannah Clarke",
        "email": "hannah@example.com",
        "postcode": "BS8 1AA",
        "project_description": "New kitchen and knock through to the dining room.",
        "preferred_contact_method": "email",
    }
    data.update(overrides)
    return data


@pytest.fixture
def broken_mail(monkeypatch):
    def fail(self, *args, **kwargs):
        raise SMTPException("Connection refused")
    monkeypatch.setattr(EmailMultiAlternatives, "send", fail)


# --- The notification function -------------------------------------------

def test_new_enquiries_start_pending():
    assert make_enquiry().notification_status == Enquiry.NotificationStatus.PENDING


def test_notification_is_sent_to_team_with_reply_to_customer(settings):
    settings.ENQUIRY_NOTIFICATION_EMAIL = "team@northstar.test"
    enquiry = make_enquiry()

    assert send_enquiry_notification(enquiry, "https://example.test/admin/1/") is True

    message = mail.outbox[0]
    assert message.to == ["team@northstar.test"]
    assert message.reply_to == ["hannah@example.com"]
    assert "Hannah Clarke" in message.subject
    assert "BS8 1AA" in message.body
    assert "https://example.test/admin/1/" in message.body
    assert message.alternatives[0].mimetype == "text/html"
    enquiry.refresh_from_db()
    assert enquiry.notification_status == Enquiry.NotificationStatus.SENT


def test_plain_text_email_is_not_html_escaped():
    enquiry = make_enquiry(name="O'Brien & Sons")
    send_enquiry_notification(enquiry)
    assert "O'Brien & Sons" in mail.outbox[0].body
    assert "&amp;" not in mail.outbox[0].body


def test_mail_failure_is_recorded_not_raised(broken_mail):
    enquiry = make_enquiry()

    assert send_enquiry_notification(enquiry) is False  # no exception escapes

    enquiry.refresh_from_db()
    assert enquiry.notification_status == Enquiry.NotificationStatus.FAILED
    assert "Connection refused" in enquiry.notification_error


# --- Through the quote form -----------------------------------------------

def test_submission_sends_one_notification(client, django_capture_on_commit_callbacks):
    with django_capture_on_commit_callbacks(execute=True):
        client.post(QUOTE_URL, valid_post())
    assert len(mail.outbox) == 1
    assert Enquiry.objects.get().notification_status == Enquiry.NotificationStatus.SENT


def test_email_includes_link_to_enquiry_in_admin(client, django_capture_on_commit_callbacks):
    with django_capture_on_commit_callbacks(execute=True):
        client.post(QUOTE_URL, valid_post())
    enquiry = Enquiry.objects.get()
    assert reverse("admin:enquiries_enquiry_change", args=[enquiry.pk]) in mail.outbox[0].body


def test_mail_failure_still_saves_enquiry_and_shows_thanks(client, broken_mail, django_capture_on_commit_callbacks):
    with django_capture_on_commit_callbacks(execute=True):
        response = client.post(QUOTE_URL, valid_post())
    assert response.status_code == 302
    assert response.url == reverse("enquiries:quote_success")
    assert Enquiry.objects.get().notification_status == Enquiry.NotificationStatus.FAILED


def test_honeypot_sends_no_email(client, django_capture_on_commit_callbacks):
    with django_capture_on_commit_callbacks(execute=True):
        client.post(QUOTE_URL, valid_post(website="http://spam.example"))
    assert len(mail.outbox) == 0


def test_duplicate_sends_no_second_email(client, django_capture_on_commit_callbacks):
    with django_capture_on_commit_callbacks(execute=True):
        client.post(QUOTE_URL, valid_post())
        client.post(QUOTE_URL, valid_post())
    assert len(mail.outbox) == 1