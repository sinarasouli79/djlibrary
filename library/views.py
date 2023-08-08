from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from library.models import Borrow
from library.serializers import CreateBorrowSerializer


# Create your views here.
class CreateBorrow(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Borrow.objects.all()
    serializer_class = CreateBorrowSerializer
