from django_filters import FilterSet, RangeFilter

from library.models import Customer


class CustomerFilter(FilterSet):
    borrow__book__borrow_inventory = RangeFilter(label='book borrow inventory')
    borrow__book__buy_inventory = RangeFilter(label='book buy inventory')

    class Meta:
        model = Customer
        fields = [
            'borrow__book__borrow_inventory',
            'borrow__book__buy_inventory',
        ]
