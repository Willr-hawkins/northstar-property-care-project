import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from enquiries.models import Enquiry, EnquiryNote, EnquiryStatusChange
from services.models import Service

pytestmark = pytest.mark.django_db

def make_enquiry(**kwargs):
    defaults = {
        "name": "Sam Example",
        "email": "sam@example.com",
        "postcode": "BS8 1AA",
        "project_description": "Kitchen extension.",
    }
    defaults.update(kwargs)
    return Enquiry.objects.create(**defaults)


# --- Status integrity ---------------------------------------------------

def test_new_enquiries_default_to_new():
    assert make_enquiry().status == Enquiry.Status.NEW

def test_database_rejects_invalid_status():
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            make_enquiry(status="archived")

def test_full_clean_rejects_invalid_status():
    enquiry = make_enquiry()
    enquiry.status = "archived"
    with pytest.raises(ValidationError):
        enquiry.full_clean()


# --- change_status ------------------------------------------------------

def test_change_status_persists_and_records_history(staff_user):
    enquiry = make_enquiry()

    assert enquiry.change_status(Enquiry.Status.CONTACTED, staff_user) is True

    enquiry.refresh_from_db()
    assert enquiry.status == Enquiry.Status.CONTACTED
    change = enquiry.status_changes.get()
    assert change.from_status == Enquiry.Status.NEW
    assert change.changed_by == staff_user

def test_change_status_to_same_status_records_nothing(staff_user):
    enquiry = make_enquiry()
    assert enquiry.change_status(Enquiry.Status.NEW, staff_user) is False
    assert EnquiryStatusChange.objects.count() == 0

def test_change_status_rejects_invalid_value(staff_user):
    enquiry = make_enquiry()
    with pytest.raises(ValueError):
        enquiry.change_status("archived", staff_user)
    enquiry.refresh_from_db()
    assert enquiry.status == Enquiry.Status.NEW
    assert EnquiryStatusChange.objects.count() == 0


# --- Notes -----------------------------------------------------------------

def test_note_belongs_to_correct_enquiry_and_author(staff_user):
    enquiry = make_enquiry()
    other = make_enquiry(name="Someone Else")
    note = EnquiryNote.objects.create(enquiry=enquiry, author=staff_user, body="Called back.")
    assert list(enquiry.notes.all()) == [note]
    assert other.notes.count() == 0
    assert note.author == staff_user


# --- Current vs former staff -----------------------------------------------------------------

def test_note_shows_current_staff_members_name(staff_user):
    staff_user.first_name, staff_user.last_name = "Sarah", "Jones"
    staff_user.save()
    note = EnquiryNote.objects.create(enquiry=make_enquiry(), author=staff_user, body="Called.")
    assert note.author_display_name == "Sarah Jones"
    assert note.author_is_former_staff is False


def test_current_staff_without_full_name_shows_username(staff_user):
    note = EnquiryNote.objects.create(enquiry=make_enquiry(), author=staff_user, body="Called.")
    assert note.author_display_name == "staff"


def test_deactivated_staff_member_shows_as_former(staff_user):
    note = EnquiryNote.objects.create(enquiry=make_enquiry(), author=staff_user, body="Called.")
    staff_user.is_active = False
    staff_user.save()
    note.refresh_from_db()
    assert note.author == staff_user  # link kept for admin records
    assert note.author_display_name == "Former staff member"
    assert note.author_is_former_staff is True


def test_deleted_staff_member_shows_as_former(staff_user):
    enquiry = make_enquiry()
    EnquiryNote.objects.create(enquiry=enquiry, author=staff_user, body="Site visit booked.")
    enquiry.change_status(Enquiry.Status.CONTACTED, staff_user)

    staff_user.delete()

    note = enquiry.notes.get()
    change = enquiry.status_changes.get()
    assert note.author is None
    assert note.author_display_name == "Former staff member"
    assert change.changed_by is None
    assert change.changed_by_display_name == "Former staff member"
    assert change.changed_by_is_former_staff is True


# --- Deletion behaviour -----------------------------------------------------

def test_deleting_service_keeps_enquiry():
    service = Service.objects.create(
        title="Extensions", short_description="x", description="x", image_alt="x"
    )
    enquiry = make_enquiry(service=service)
    service.delete()
    enquiry.refresh_from_db()
    assert enquiry.service is None


def test_deleting_enquiry_removes_notes_and_history(staff_user):
    enquiry = make_enquiry()
    EnquiryNote.objects.create(enquiry=enquiry, author=staff_user, body="Note.")
    enquiry.change_status(Enquiry.Status.QUOTED, staff_user)
    enquiry.delete()
    assert EnquiryNote.objects.count() == 0
    assert EnquiryStatusChange.objects.count() == 0