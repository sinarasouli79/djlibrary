from django_filters import FilterSet, RangeFilter

from library.models import Customer, Book


class CustomerFilter(FilterSet):
    borrow__book__borrow_inventory = RangeFilter(label='book borrow inventory')
    borrow__book__buy_inventory = RangeFilter(label='book buy inventory')

    class Meta:
        model = Customer
        fields = [
            'borrow__book__borrow_inventory',
            'borrow__book__buy_inventory',
        ]


class BookFilter(FilterSet):
    borrow_inventory = RangeFilter()
    buy_inventory = RangeFilter()
    buy_price = RangeFilter()

    class Meta:
        model = Book
        fields = ['collection', 'borrow_inventory', 'buy_inventory', 'buy_price'
                  ]
