import pytest

from services.models import Service

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
