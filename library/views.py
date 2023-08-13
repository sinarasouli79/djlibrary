from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from library.models import Borrow, Customer
from library.permissions import IsLibrarian
from library.serializers import CreateBorrowSerializer, UpdateBorrowSerializer, CustomerListSerializer


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
