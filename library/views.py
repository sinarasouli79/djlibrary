from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.decorators import api_view, action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from library.filters import CustomerFilter, BookFilter
from library.models import Borrow, Customer, Buy, Collection, Book
from library.permissions import IsLibrarian
from library.serializers import CreateBorrowSerializer, UpdateBorrowSerializer, CustomerListSerializer, \
    CreateBuySerializer, BookSerializer


# Create your views here.
class BorrowViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    GenericViewSet):
    permission_classes = [IsAuthenticated, IsLibrarian]
    http_method_names = ['patch', 'post', 'head', 'options']

    def get_queryset(self):

        if self.request.method == 'PATCH':
            return Borrow.objects.filter(actual_return_date__isnull=True)
        else:
            return Borrow.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdateBorrowSerializer
        else:
            return CreateBorrowSerializer


class CustomerListView(mixins.ListModelMixin,
                       GenericViewSet):
    permission_classes = [IsAuthenticated, IsLibrarian]
    queryset = Customer.objects.select_related('user').prefetch_related('borrow_set__book__collection').all()
    serializer_class = CustomerListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CustomerFilter
    search_fields = ['borrow__book__title', 'borrow__book__collection__title', ]


class BuyCreateView(mixins.CreateModelMixin,
                    GenericViewSet):
    permission_classes = [IsAuthenticated, IsLibrarian]
    queryset = Buy.objects.all()
    serializer_class = CreateBuySerializer


class BookViewSet(mixins.ListModelMixin,
                  GenericViewSet):
    permission_classes = [IsAuthenticated, IsLibrarian]
    queryset = Book.objects.select_related('collection').all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = BookFilter
    search_fields = ['title', 'collection__title', ]

    @action(detail=False)
    def buyable(self, request):
        queryset = Book.objects.select_related('collection').filter(buy_inventory__gt=0)
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view()
def report(request, *args, **kwargs):  # todo add permissions
    collections_profit = {}
    collections = Collection.objects.all()
    for collection in collections:
        collections_profit[collection.title] = {'borrow': 0, 'buy': 0}

    borrows = Borrow.objects.select_related('book__collection')
    for borrow in borrows:
        collections_profit[borrow.book.collection.title]['borrow'] += borrow.book.collection.borrow_price

    buys = Buy.objects.select_related('book__collection')
    for buy in buys:
        collections_profit[buy.book.collection.title]['buy'] += buy.book.buy_price

    return Response(collections_profit)
