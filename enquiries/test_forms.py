import pytest

from enquiries.forms import QuoteForm
from enquiries.models import Enquiry
from services.models import Service

pytestmark = pytest.mark.django_db


def valid_data(**overrides):
    data = {
        "name": "Hannah Clarke",
        "email": "Hannah.Clarke@Example.com",
        "phone": "",
        "service": "",
        "postcode": "bs81aa",
        "project_description": "New kitchen and knock through to the dining room.",
        "preferred_contact_method": "email",
    }
    data.update(overrides)
    return data


def test_valid_form_saves_and_normalises():
    form = QuoteForm(data=valid_data())
    assert form.is_valid(), form.errors
    enquiry = form.save()
    assert enquiry.postcode == "BS8 1AA"
    assert enquiry.email == "hannah.clarke@example.com"
    assert enquiry.status == Enquiry.Status.NEW
    assert enquiry.service is None


@pytest.mark.parametrize("postcode", ["BS8", "12345", "ABC 123", "BS8 1A"])
def test_invalid_postcodes_are_rejected(postcode):
    form = QuoteForm(data=valid_data(postcode=postcode))
    assert not form.is_valid()
    assert form.errors["postcode"] == ["Enter a valid UK postcode, like BS8 1AA"]


@pytest.mark.parametrize("phone", ["07700 900123", "+44 7700 900123", "0117 496 0123"])
def test_valid_uk_phone_numbers_are_accepted(phone):
    assert QuoteForm(data=valid_data(phone=phone)).is_valid()


def test_invalid_phone_is_rejected():
    form = QuoteForm(data=valid_data(phone="12345"))
    assert "phone" in form.errors


def test_phone_required_when_phone_is_preferred():
    form = QuoteForm(data=valid_data(preferred_contact_method="phone"))
    assert form.errors["phone"] == ["Enter a phone number, or choose email as your contact method"]


def test_short_description_is_rejected():
    form = QuoteForm(data=valid_data(project_description="Kitchen"))
    assert "project_description" in form.errors


def test_inactive_services_cannot_be_chosen():
    hidden = Service.objects.create(title="Hidden", short_description="x", description="x", image_alt="x", is_active=False)
    form = QuoteForm(data=valid_data(service=hidden.pk))
    assert "service" in form.errors


def test_invalid_fields_are_linked_to_their_errors():
    form = QuoteForm(data=valid_data(postcode="nope"))
    form.is_valid()
    attrs = form.fields["postcode"].widget.attrs
    assert attrs["aria-invalid"] == "true"
    assert attrs["aria-describedby"] == "id_postcode_error"


def test_honeypot_marks_submission_as_spam():
    form = QuoteForm(data=valid_data(website="http://spam.example"))
    assert form.is_valid()
    assert form.is_spam()


def test_honeypot_empty_is_not_spam():
    form = QuoteForm(data=valid_data())
    assert form.is_valid()
    assert not form.is_spam()