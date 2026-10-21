import pytest

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