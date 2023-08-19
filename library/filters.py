from django.db.models import Count
from django_filters import FilterSet, NumberFilter

from library.models import Book, Borrow


class BookFilter(FilterSet):
    borrow_count_gte = NumberFilter(label='borrow_count_gte', method='filter_borrow_count')
    borrow_count_lte = NumberFilter(label='borrow_count_lte', method='filter_borrow_count')

    def filter_borrow_count(self, queryset, name, value):
        queryset = queryset.annotate(borrow_count=Count('borrow'))
        if name == 'borrow_count_gte':
            queryset = queryset.filter(borrow_count__gte=value)
        else:
            queryset = queryset.filter(borrow_count__lte=value)
        return queryset

    class Meta:
        model = Book
        fields = {'collection': ['exact', ],
                  'borrow_inventory': ['gte', 'lte'],
                  'buy_inventory': ['gte', 'lte'],
                  'buy_price': ['gte', 'lte'],
                  }


class BorrowFilter(FilterSet):
    class Meta:
        model = Borrow
        fields = {
            'borrow_date': ['gte', 'lte'],
            'expected_return_date': ['gte', 'lte'],
            'actual_return_date': ['gte', 'lte', 'isnull'],
            'book__borrow_inventory': ['gte', 'lte'],
            'book__buy_inventory': ['gte', 'lte'],
            'book__buy_price': ['gte', 'lte'],
            'book__collection__borrow_price': ['gte', 'lte'],
            'book__collection__borrow_limit': ['gte', 'lte'],
            'customer': ['exact']
        }
