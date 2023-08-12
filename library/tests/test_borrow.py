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
            min_customer_balance = book.collection.borrow_price * 3
            customer = baker.make('library.Customer', balance=min_customer_balance)

            if not data:
                tomorrow = datetime.date.today() + datetime.timedelta(1)
                data = {'book': book.id, 'customer': customer.id,
                        'expected_return_date': tomorrow,
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
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_user_brakes_collection_borrow_limit_rule_return_400(self, create_borrow):
        collection = baker.make('library.Collection', borrow_limit=3)
        books = baker.make('library.Book', collection=collection, _quantity=4)
        customer = baker.make('library.Customer')
        # already_borrowed_book = baker.make('library.borrow', collection=collection)
        for book in books[:3]:
            baker.make('library.Borrow', book_id=book.id, customer=customer)

        #  borrowing this book bakes the rule because the borrow limit of the collection is 3
        #  and the customer already borrowed 3 books.
        new_borrow_book = baker.make('library.Book', collection=collection)
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        data = {'book': new_borrow_book.id, 'customer': customer.id,
                'expected_return_date': tomorrow
            ,
                }

        response = create_borrow(is_librarian=True, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_brakes_maximum_borrow_date_return_400(self, create_borrow):
        # arrange
        book = baker.make('library.book', borrow_inventory=2)
        min_customer_balance = book.collection.borrow_price * 3
        customer = baker.make('library.Customer', balance=min_customer_balance)
        print(customer.id)
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        data = {
            'book': book.id,
            'customer': customer.id,
            'expected_return_date': tomorrow,
        }

        customer = baker.make('library.Customer', balance=min_customer_balance)
        create_borrow(is_librarian=True, data=data)
        next_year = datetime.date.today() + datetime.timedelta(days=365)
        data = {
            'book': book.id,
            'customer': customer.id,
            'expected_return_date': next_year
        }
        response = create_borrow(is_librarian=True, data=data)
        print(response.data)
        # assert False
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['expected_return_date'] is not None

    def test_if_book_inventory_is_low_return_400(self, create_borrow):
        book = baker.make('library.Book', borrow_inventory=0)
        min_customer_balance = book.collection.borrow_price * 3
        customer = baker.make('library.Customer', balance=min_customer_balance)
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        data = {
            'book': book.id,
            'customer': customer.id,
            'expected_return_date': tomorrow,
        }
        response = create_borrow(is_librarian=True, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['book'] is not None

    def test_if_customer_is_ban_return_400(self, create_borrow):
        book = baker.make('library.Book', borrow_inventory=1)
        min_customer_balance = book.collection.borrow_price * 3
        customer = baker.make('library.Customer', balance=min_customer_balance, is_ban=True)
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        data = {
            'book': book.id,
            'customer': customer.id,
            'expected_return_date': tomorrow,
        }
        response = create_borrow(is_librarian=True, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['customer'] is not None

    def test_if_customer_balance_is_low_return_400(self, create_borrow):
        book = baker.make('library.Book', borrow_inventory=1)
        min_customer_balance = book.collection.borrow_price * 3
        customer = baker.make('library.Customer', balance=min_customer_balance - 1)
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        data = {
            'book': book.id,
            'customer': customer.id,
            'expected_return_date': tomorrow,
        }
        response = create_borrow(is_librarian=True, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['customer'] is not None
   