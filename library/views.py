from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from library.models import Borrow
from library.permissions import IsLibrarian
from library.serializers import CreateBorrowSerializer, UpdateBorrowSerializer


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
