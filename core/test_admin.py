import pytest
from django.urls import reverse

from enquiries.models import Enquiry, EnquiryNote
from services.models import Service

pytestmark = pytest.mark.django_db


def make_enquiry():
    return Enquiry.objects.create(
        name="Sam Example", email="sam@example.com",
        postcode="BS8 1AA", project_description="Kitchen extension.",
    )


NOTES_MANAGEMENT = {
    "notes-TOTAL_FORMS": "0",
    "notes-INITIAL_FORMS": "0",
    "notes-MIN_NUM_FORMS": "0",
    "notes-MAX_NUM_FORMS": "1000",
}

@pytest.mark.parametrize("url_name", [
    "admin:services_service_changelist",
    "admin:projects_project_changelist",
    "admin:enquiries_enquiry_changelist",
    "admin:services_service_add",
    "admin:projects_project_add",
])
def test_admin_pages_load(admin_client, url_name):
    assert admin_client.get(reverse(url_name)).status_code == 200

def test_enquiries_cannot_be_added_in_admin(admin_client):
    response = admin_client.get(reverse("admin:enquiries_enquiry_add"))
    assert response.status_code == 403

def test_enquiry_detail_page_loads(admin_client):
    enquiry = make_enquiry()
    url = reverse("admin:enquiries_enquiry_change", args=[enquiry.pk])
    assert admin_client.get(url).status_code == 200

def test_admin_status_change_records_history(admin_client, admin_user):
    enquiry = make_enquiry()
    url =reverse("admin:enquiries_enquiry_change", args=[enquiry.pk])

    response = admin_client.post(url, {"status": "contacted", **NOTES_MANAGEMENT})

    assert response.status_code == 302  # redirect = saved successfully
    enquiry.refresh_from_db()
    assert enquiry.status == Enquiry.Status.CONTACTED
    change = enquiry.status_changes.get()
    assert change.changed_by == admin_user

def test_admin_note_is_signed_by_logged_in_user(admin_client, admin_user):
    enquiry = make_enquiry()
    url = reverse("admin:enquiries_enquiry_change", args=[enquiry.pk])

    data = {
        "status": "new",
        **NOTES_MANAGEMENT,
        "notes-TOTAL_FORMS": "1",
        "notes-0-body": "Called to book a site visit.",
    }
    response = admin_client.post(url, data)

    assert response.status_code == 302
    note = EnquiryNote.objects.get()
    assert note.enquiry == enquiry
    assert note.author == admin_user