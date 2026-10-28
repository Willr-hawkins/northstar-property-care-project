import pytest

from django.urls import reverse

from services.models import Service
from projects.models import Project


pytestmark = pytest.mark.django_db


def make_service(**kwargs):
    defaults = {
        "title": "Home renovations",
        "short_description": "Whole-house renovations.",
        "description": "Full description.",
        "image_alt": "Renovated living room",
    }
    defaults.update(kwargs)
    return Service.objects.create(**defaults)


def test_slug_is_generated_from_title():
    assert make_service(title="Kitchens & Bathrooms").slug == "kitchens-bathrooms"


def test_active_excludes_inactive_services():
    live = make_service(title="Live")
    make_service(title="Hidden", is_active=False)
    assert list(Service.objects.active()) == [live]


def test_services_ordered_by_display_order_then_title():
    b = make_service(title="B", display_order=2)
    a = make_service(title="A", display_order=2)
    first = make_service(title="Z", display_order=1)
    assert list(Service.objects.all()) == [first, a, b]


def test_service_list_shows_only_active_services_in_order(client):
    second = make_service(title="Second", display_order=2)
    first = make_service(title="First", display_order=1)
    make_service(title="Hidden", is_active=False)
    response = client.get(reverse("services:list"))
    assert response.status_code == 200
    assert list(response.context["services"]) == [first, second]
    assert "Hidden" not in response.content.decode()


def test_service_detail_returns_200_for_active_service(client):
    service = make_service(title="Kitchens")
    response = client.get(service.get_absolute_url())
    assert response.status_code == 200
    assert response.context["service"] == service


def test_inactive_service_detail_returns_404(client):
    service = make_service(title="Hidden", is_active=False)
    assert client.get(service.get_absolute_url()).status_code == 404


def test_service_number_matches_position_among_active_services(client):
    make_service(title="One", display_order=1)
    make_service(title="Hidden", display_order=2, is_active=False)
    third = make_service(title="Three", display_order=3)
    response = client.get(third.get_absolute_url())
    assert response.context["number"] == 2  # hidden service doesn't count


def test_related_projects_are_published_and_belong_to_service(client):
    service = make_service(title="Kitchens")
    other = make_service(title="Extensions")
    common = {"summary": "x", "description": "x", "featured_image_alt": "x", "category": Project.Category.KITCHEN}
    shown = Project.objects.create(title="Shown", service=service, is_published=True, **common)
    Project.objects.create(title="Draft", service=service, is_published=False, **common)
    Project.objects.create(title="Elsewhere", service=other, is_published=True, **common)
    response = client.get(service.get_absolute_url())
    assert list(response.context["related_projects"]) == [shown]