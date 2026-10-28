import pytest
from django.urls import reverse

from projects.models import Project
from services.models import Service

pytestmark = pytest.mark.django_db


def test_home_page_returns_200(client):
    response = client.get(reverse("core:home"))
    assert response.status_code == 200


def test_home_page_uses_base_template(client):
    response = client.get(reverse("core:home"))
    template_names = [t.name for t in response.templates]
    assert "core/home.html" in template_names
    assert "base.html" in template_names


def test_base_template_has_accessiblity_and_htmx_essentials(client):
    content = client.get(reverse("core:home")).content.decode()
    assert 'href="#main"' in content              # skip link
    assert 'id="main"' in content                 # skip link target
    assert 'id="messages"' in content             # HTMX out-of-band message target
    assert "X-CSRFToken" in content               # global HTMX CSRF header
    assert '<link rel="canonical"' in content


def make_service(**kwargs):
    defaults = {"title": "Kitchens", "short_description": "x", "description": "x", "image_alt": "x"}
    defaults.update(kwargs)
    return Service.objects.create(**defaults)


def make_project(**kwargs):
    defaults = {
        "title": "Project", "category": Project.Category.KITCHEN,
        "summary": "x", "description": "x", "featured_image_alt": "x",
        "is_published": True, "is_featured": True,
    }
    defaults.update(kwargs)
    return Project.objects.create(**defaults)


def test_home_lists_only_active_services(client):
    make_service(title="Visible Service")
    make_service(title="Hidden Service", is_active=False)
    content = client.get(reverse("core:home")).content.decode()
    assert "Visible Service" in content
    assert "Hidden Service" not in content


def test_home_shows_only_published_featured_projects(client):
    make_project(title="Live Featured")
    make_project(title="Draft Featured", is_published=False)
    make_project(title="Live Not Featured", is_featured=False)
    content = client.get(reverse("core:home")).content.decode()
    assert "Live Featured" in content
    assert "Draft Featured" not in content
    assert "Live Not Featured" not in content


def test_home_shows_at_most_three_featured_projects(client):
    for i in range(5):
        make_project(title=f"Featured {i}", slug=f"featured-{i}")
    response = client.get(reverse("core:home"))
    assert len(response.context["featured_projects"]) == 3


def test_home_renders_with_no_content(client):
    response = client.get(reverse("core:home"))
    assert response.status_code == 200
    assert response.context["hero_project"] is None