import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from projects.models import Project, ProjectImage
from services.models import Service

pytestmark = pytest.mark.django_db


def make_project(**kwargs):
    defaults = {
        "title": "The Orchard House",
        "category": Project.Category.EXTENSION,
        "summary": "Rear extension.",
        "description": "Full description.",
        "featured_image_alt": "Glazed rear extension",
    }
    defaults.update(kwargs)
    return Project.objects.create(**defaults)


def test_projects_are_unpublished_by_default():
    assert make_project().is_published is False


def test_published_excludes_drafts():
    live = make_project(title="Live", is_published=True)
    make_project(title="Draft")
    assert list(Project.objects.published()) == [live]


def test_featured_requires_published():
    make_project(title="Featured draft", is_featured=True)
    shown = make_project(title="Featured live", is_featured=True, is_published=True)
    assert list(Project.objects.featured()) == [shown]


def test_deleting_service_keeps_project():
    service = Service.objects.create(
        title="Extensions", short_description="x", description="x", image_alt="x"
    )
    project = make_project(service=service)
    service.delete()
    project.refresh_from_db()
    assert project.service is None


def test_deleting_project_deletes_its_images():
    project = make_project()
    ProjectImage.objects.create(project=project, alt_text="Before", kind=ProjectImage.Kind.BEFORE)
    project.delete()
    assert ProjectImage.objects.count() == 0

# A valid 1x1 pixel GIF, so image fields have a real file to render.
TINY_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00"
    b"\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)


@pytest.fixture
def image_file(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    return lambda name="photo.gif": SimpleUploadedFile(name, TINY_GIF, content_type="image/gif")


def titles(response):
    return [p.title for p in response.context["projects"]]


# --- Gallery -------------------------------------------------------------

def test_project_list_shows_only_published(client):
    make_project(title="Live", is_published=True)
    make_project(title="Draft")
    assert titles(client.get(reverse("projects:list"))) == ["Live"]


def test_project_list_filters_by_category(client):
    make_project(title="Kitchen One", category=Project.Category.KITCHEN, is_published=True)
    make_project(title="Bath One", category=Project.Category.BATHROOM, is_published=True)
    response = client.get(reverse("projects:list"), {"category": "kitchen"})
    assert titles(response) == ["Kitchen One"]
    assert response.context["active_category"] == "kitchen"


def test_unknown_category_shows_everything(client):
    make_project(title="Kitchen One", category=Project.Category.KITCHEN, is_published=True)
    make_project(title="Bath One", category=Project.Category.BATHROOM, is_published=True)
    response = client.get(reverse("projects:list"), {"category": "spaceships"})
    assert len(titles(response)) == 2
    assert response.context["active_category"] == ""


def test_category_counts_ignore_drafts(client):
    make_project(title="Live Kitchen", category=Project.Category.KITCHEN, is_published=True)
    make_project(title="Draft Kitchen", category=Project.Category.KITCHEN)
    response = client.get(reverse("projects:list"))
    counts = {c["key"]: c["count"] for c in response.context["categories"]}
    assert counts[""] == 1
    assert counts["kitchen"] == 1
    assert counts["bathroom"] == 0


def test_empty_category_shows_empty_state(client):
    make_project(title="Kitchen One", category=Project.Category.KITCHEN, is_published=True)
    response = client.get(reverse("projects:list"), {"category": "bathroom"})
    assert "No bathroom projects to show yet." in response.content.decode()


# --- HTMX ------------------------------------------------------------------

def template_names(response):
    return [t.name for t in response.templates]


def test_htmx_request_returns_results_fragment(client):
    response = client.get(reverse("projects:list"), {"category": "kitchen"}, headers={"HX-Request": "true"})
    assert "projects/partials/project_results.html" in template_names(response)
    assert "base.html" not in template_names(response)
    assert 'id="results-summary"' in response.content.decode()
    assert 'hx-swap-oob="true"' in response.content.decode()


def test_htmx_history_restore_returns_full_page(client):
    headers = {"HX-Request": "true", "HX-History-Restore-Request": "true"}
    response = client.get(reverse("projects:list"), headers=headers)
    assert "base.html" in template_names(response)


def test_normal_request_returns_full_page_without_oob(client):
    response = client.get(reverse("projects:list"))
    assert "base.html" in template_names(response)
    assert "projects/partials/project_results.html" in template_names(response)
    assert 'hx-swap-oob="true"' not in response.content.decode()


# --- Detail ----------------------------------------------------------------

def test_published_project_detail_returns_200(client):
    project = make_project(title="Live", is_published=True)
    assert client.get(project.get_absolute_url()).status_code == 200


def test_draft_project_detail_returns_404(client):
    project = make_project(title="Draft")
    assert client.get(project.get_absolute_url()).status_code == 404


def test_detail_builds_before_after_and_gallery(client, image_file):
    project = make_project(title="Orchard", is_published=True)
    ProjectImage.objects.create(project=project, kind="before", alt_text="Old kitchen", image=image_file("b.gif"))
    ProjectImage.objects.create(project=project, kind="after", alt_text="New kitchen", image=image_file("a.gif"))
    ProjectImage.objects.create(project=project, kind="gallery", alt_text="Detail", image=image_file("g.gif"))
    response = client.get(project.get_absolute_url())
    assert response.context["before_image"].alt_text == "Old kitchen"
    assert response.context["after_image"].alt_text == "New kitchen"
    assert [i.alt_text for i in response.context["gallery_images"]] == ["Detail"]
    assert "data-before-after" in response.content.decode()


def test_lone_before_image_goes_to_gallery_without_slider(client, image_file):
    project = make_project(title="Solo", is_published=True)
    ProjectImage.objects.create(project=project, kind="before", alt_text="Old kitchen", image=image_file())
    response = client.get(project.get_absolute_url())
    assert response.context["before_image"] is None
    assert [i.alt_text for i in response.context["gallery_images"]] == ["Old kitchen"]
    assert "data-before-after" not in response.content.decode()