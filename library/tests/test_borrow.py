import pytest
from model_bakery import baker
from rest_framework import status


@pytest.mark.django_db
class TestCreateBorrow:
    def test_if_user_is_anonymous_return_401(self, api_client):
        book = baker.make('library.Book')
        customer = baker.make('library.Customer')
        response = api_client.post('/library/borrow/', {'book': book.id, 'customer': customer.id})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
