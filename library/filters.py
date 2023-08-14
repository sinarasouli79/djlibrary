from django_filters import FilterSet, RangeFilter, NumberFilter

from library.models import Customer, Book


class CustomerFilter(FilterSet):
    borrow__book__borrow_inventory = RangeFilter(label='book borrow inventory')
    borrow__book__buy_inventory = RangeFilter(label='book buy inventory')

    penalties_count = NumberFilter(label='penalties_count_gte', method='filter_penalties_count')

    def filter_penalties_count(self, queryset, name, value):
        queryset = queryset.filter(penalties_count__gte=value)
        return queryset

    class Meta:
        model = Customer
        fields = [
            'borrow__book__borrow_inventory',
            'borrow__book__buy_inventory',
            'penalties_count'
        ]


class BookFilter(FilterSet):
    borrow_inventory = RangeFilter()
    buy_inventory = RangeFilter()
    buy_price = RangeFilter()

    class Meta:
        model = Book
        fields = ['collection', 'borrow_inventory', 'buy_inventory', 'buy_price'
                  ]
