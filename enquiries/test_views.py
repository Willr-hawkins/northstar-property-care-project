import pytest
from django.urls import reverse
from django.utils import timezone

from datetime import timedelta

from enquiries.models import Enquiry
from services.models import Service

pytestmark = pytest.mark.django_db

QUOTE_URL = reverse("enquiries:quote")


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


def make_service(**kwargs):
    defaults = {"title": "Kitchens", "short_description": "x", "description": "x", "image_alt": "x"}
    defaults.update(kwargs)
    return Service.objects.create(**defaults)


def test_quote_page_loads_with_privacy_link(client):
    response = client.get(QUOTE_URL)
    assert response.status_code == 200
    assert reverse("core:privacy") in response.content.decode()


def test_service_query_param_preselects_active_service(client):
    service = make_service(slug="kitchens")
    response = client.get(QUOTE_URL, {"service": "kitchens"})
    assert response.context["form"].initial["service"] == service.pk


def test_inactive_service_query_param_is_ignored(client):
    make_service(slug="hidden", is_active=False)
    response = client.get(QUOTE_URL, {"service": "hidden"})
    assert "service" not in response.context["form"].initial


def test_valid_submission_saves_and_redirects_to_thanks(client):
    response = client.post(QUOTE_URL, valid_post())
    assert response.status_code == 302
    assert response.url == reverse("enquiries:quote_success")
    assert Enquiry.objects.count() == 1

    thanks = client.get(response.url)
    assert "Thank you, Hannah Clarke." in thanks.content.decode()


def test_invalid_submission_shows_errors_and_saves_nothing(client):
    response = client.post(QUOTE_URL, valid_post(email="not-an-email", postcode="nope"))
    content = response.content.decode()
    assert response.status_code == 200
    assert Enquiry.objects.count() == 0
    assert 'id="error-summary"' in content
    assert "There's a problem with 2 fields" in content
    assert 'aria-invalid="true"' in content


def test_thanks_page_redirects_without_a_submission(client):
    response = client.get(reverse("enquiries:quote_success"))
    assert response.status_code == 302
    assert response.url == QUOTE_URL


def test_thanks_page_only_shows_once(client):
    client.post(QUOTE_URL, valid_post())
    client.get(reverse("enquiries:quote_success"))
    second = client.get(reverse("enquiries:quote_success"))
    assert second.status_code == 302


def test_every_quote_button_on_the_homepage_links_to_the_form(client):
    content = client.get(reverse("core:home")).content.decode()
    assert content.count(f'href="{QUOTE_URL}"') >= 3  # header (desktop + mobile), hero, CTA band


def test_honeypot_submission_is_discarded_but_looks_successful(client):
    response = client.post(QUOTE_URL, valid_post(website="http://spam.example"))
    assert response.status_code == 302
    assert response.url == reverse("enquiries:quote_success")
    assert Enquiry.objects.count() == 0


def test_identical_resubmission_within_window_is_saved_once(client):
    client.post(QUOTE_URL, valid_post())
    response = client.post(QUOTE_URL, valid_post())
    assert response.status_code == 302
    assert Enquiry.objects.count() == 1


def test_different_project_from_same_person_is_saved(client):
    client.post(QUOTE_URL, valid_post())
    client.post(QUOTE_URL, valid_post(project_description="We'd also like a quote for a loft conversion."))
    assert Enquiry.objects.count() == 2


def test_identical_submission_after_window_is_saved(client):
    client.post(QUOTE_URL, valid_post())
    Enquiry.objects.update(created_at=timezone.now() - timedelta(minutes=30))
    client.post(QUOTE_URL, valid_post())
    assert Enquiry.objects.count() == 2


def test_form_has_submit_once_and_hidden_honeypot(client):
    content = client.get(QUOTE_URL).content.decode()
    assert "data-submit-once" in content
    assert "js/forms.js" in content
    assert 'name="website"' in content
    assert 'tabindex="-1"' in content