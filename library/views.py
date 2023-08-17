from django.db.models import Count
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from library.filters import CustomerFilter, BookFilter, BorrowFilter
from library.models import Borrow, Customer, Buy, Collection, Book
from library.permissions import IsLibrarian
from library.serializers import CreateBorrowSerializer, UpdateBorrowSerializer, CustomerListSerializer, \
    CreateBuySerializer, BookSerializer, CustomerPenaltiesListSerializer, BorrowListSerializer, CollectionSerializer, \
    BuySerializer


# Create your views here.
class BorrowViewSet(ModelViewSet):
    http_method_names = ['patch', 'get', 'post', 'delete', 'head', 'options']
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['book__title', 'book__collection__title', 'customer__user__first_name',
                     'customer__user__last_name']
    filterset_class = BorrowFilter

    def get_queryset(self):
        user_is_librarian = self.request.user.is_librarian
        queryset = Borrow.objects.select_related('customer__user', 'book__collection')
        if self.request.method == 'PATCH':
            queryset = queryset.filter(actual_return_date__isnull=True)
        elif self.request.method in ['POST', 'GET']:
            if not user_is_librarian:
                queryset = queryset.filter(customer__user=self.request.user)

        return queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), IsLibrarian()]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdateBorrowSerializer
        if self.request.method == 'GET':
            return BorrowListSerializer
        else:
            return CreateBorrowSerializer


class CustomerListView(mixins.ListModelMixin,
                       GenericViewSet):
    permission_classes = [IsAuthenticated, IsLibrarian]
    queryset = Customer.objects.select_related('user').prefetch_related('borrow_set__book__collection',
                                                                        'penalties_set', ).all().annotate(
        penalties_count=Count('penalties'), borrow_count=Count('borrow'))
    serializer_class = CustomerListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CustomerFilter
    search_fields = ['borrow__book__title', 'borrow__book__collection__title', ]

    @action(detail=False)
    def penalties(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CustomerPenaltiesListSerializer(queryset, many=True)
        return Response(serializer.data)


class BuyViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['^customer__user__first_name', '^customer__user__last_name', '^customer__user__username',
                     '^book__title']

    def get_queryset(self):
        user = self.request.user
        queryset = Buy.objects.select_related('book__collection', 'customer__user').all()
        if not user.is_librarian:
            queryset = queryset.filter(customer__user=user)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BuySerializer

        return CreateBuySerializer

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            return [IsAuthenticated(), IsLibrarian()]
        return [IsAuthenticated()]


class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('collection').prefetch_related('borrow_set').annotate(
        borrow_count=Count('borrow'))
    serializer_class = BookSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = BookFilter
    search_fields = ['title', 'collection__title', ]
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAuthenticated(), IsLibrarian()]
        else:
            return [IsAuthenticated()]

    @action(detail=False)
    def buyable(self, request):
        queryset = Book.objects.select_related('collection').filter(buy_inventory__gt=0)
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), IsLibrarian()]


@api_view()
@permission_classes([IsAuthenticated, IsLibrarian])
def report(request, *args, **kwargs):
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
