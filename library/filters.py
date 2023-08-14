from django_filters import FilterSet, NumberFilter

from library.models import Customer, Book


class CustomerFilter(FilterSet):
    borrow__book__borrow_inventory_gte = NumberFilter(label='borrow__book__borrow_inventory_gte', lookup_expr='gte')
    borrow__book__borrow_inventory_lte = NumberFilter(label='borrow__book__borrow_inventory_lte', lookup_expr='lte')
    borrow__book__buy_inventory_gte = NumberFilter(label='borrow__book__buy_inventory_gte', lookup_expr='gte')
    borrow__book__buy_inventory_lte = NumberFilter(label='borrow__book__buy_inventory_lte', lookup_expr='lte')

    penalties_count_gte = NumberFilter(label='penalties_count_gte', lookup_expr='gte', method='filter_penalties_count')

    def filter_penalties_count(self, queryset, name, value):
        queryset = queryset.filter(penalties_count__gte=value)
        return queryset

    class Meta:
        model = Customer
        fields = [
            'borrow__book__borrow_inventory_gte',
            'borrow__book__borrow_inventory_lte',
            'borrow__book__buy_inventory_gte',
            'borrow__book__buy_inventory_lte',
            'penalties_count_gte'
        ]


class BookFilter(FilterSet):
    class Meta:
        model = Book
        fields = {'collection': ['gte', 'lte'], 'borrow_inventory': ['gte', 'lte'], 'buy_inventory': ['gte', 'lte'],
                  'buy_price': ['gte', 'lte']
                  }
