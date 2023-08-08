from rest_framework import serializers

from library.models import Borrow


class CreateBorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['id', 'book', 'customer', 'borrow_date', 'expected_return_date', 'actual_return_date']
