import pytest
from django.contrib.auth import get_user_model

@pytest.fixture
def user(db):
    """ An ordinary logged-out-style user with no staff access. """
    return get_user_model().objects.create_user(
        username="visitor", email="visitor@example.com", password="test-pass-123"
    )

@pytest.fixture
def staff_user(db):
    """ A staff user. The Staff group and its permissions are added in Sprint 4. """
    return get_user_model().objects.create_user(
        username="staff", email="staff@example.com", password="test-pass-123", is_staff=True
    )

@pytest.fixture
def staff_client(client, staff_user):
    """ Django test client aleady logged in as staff. """
    client.force_login(staff_user)
    return client