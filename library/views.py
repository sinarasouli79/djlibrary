from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from library.filters import CustomerFilter
from library.models import Borrow, Customer, Buy
from library.permissions import IsLibrarian
from library.serializers import CreateBorrowSerializer, UpdateBorrowSerializer, CustomerListSerializer, \
    CreateBuySerializer


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
