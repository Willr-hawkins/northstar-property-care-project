import pytest
from django.urls import reverse

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