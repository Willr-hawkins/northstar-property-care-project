import pytest
from django.urls import reverse
from django.template.loader import render_to_string

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


def test_about_page_returns_200(client):
    response = client.get(reverse("core:about"))
    assert response.status_code == 200
    assert "core/about.html" in [t.name for t in response.templates]


def test_about_page_labels_team_as_fictional(client):
    content = client.get(reverse("core:about")).content.decode()
    assert "Sarah Jones" in content
    assert "Team members are fictional" in content


def test_unknown_url_uses_custom_404(client):
    response = client.get("/this-page-does-not-exist/")
    assert response.status_code == 404
    assert "404.html" in [t.name for t in response.templates]
    assert "We can't find this page." in response.content.decode()


def test_500_templates_renders_without_any_context():
    # Django renders 500.html with no request or context processors, so it must stand alone.
    html = render_to_string("500.html")
    assert "Something went wrong" in html
    assert "{%" not in html and "{{" not in html


def test_privacy_page_lists_what_the_form_collects(client):
    content = client.get(reverse("core:privacy")).content.decode()
    assert "What we collect" in content
    assert "postcode" in content
    assert "portfolio demo" in content


def test_footer_links_to_privacy_notice(client):
    content = client.get(reverse("core:home")).content.decode()
    assert f'href="{reverse("core:privacy")}"' in content