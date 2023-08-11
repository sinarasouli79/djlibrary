import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from core.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def _authenticate(is_anonymous=False, is_librarian=False):
        if not is_anonymous:
            if is_librarian:
                librarian = baker.make('library.Librarian')
                user = User.objects.get(id=librarian.user_id)  # todo not import core
            else:
                user = baker.make('core.User')
        else:
            user = None
        return api_client.force_authenticate(user=user)

    return _authenticate
