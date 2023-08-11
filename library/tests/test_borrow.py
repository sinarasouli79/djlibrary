import datetime

import pytest
from model_bakery import baker
from rest_framework import status


@pytest.mark.django_db
class TestCreateBorrow:
    @pytest.fixture
    def create_borrow(self, api_client, authenticate):
        def _create_borrow(is_anonymous=False, is_librarian=False, data=None):
            authenticate(is_anonymous=is_anonymous, is_librarian=is_librarian)
            book = baker.make('library.Book')
            customer = baker.make('library.Customer')

            if not data:
                data = {'book': book.id, 'customer': customer.id,
                        'expected_return_date': datetime.datetime.now(),
                        }

            return api_client.post('/library/borrow/', data=data)

        return _create_borrow

    def test_if_user_is_anonymous_return_401(self, api_client, create_borrow):
        response = create_borrow(is_anonymous=True)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_librarian_return_403(self, create_borrow):
        response = create_borrow(is_librarian=False)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_librarian_and_data_is_valid_return_201(self, create_borrow):
        response = create_borrow(is_librarian=True)
        assert response.status_code == status.HTTP_201_CREATED
