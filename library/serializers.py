import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from library.models import Borrow, Collection, Penalties, Customer, Book, Buy


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'borrow_price', 'borrow_limit']


class BookSerializer(serializers.ModelSerializer):
    collection = CollectionSerializer(read_only=True)
    borrow_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'borrow_inventory', 'buy_inventory', 'buy_price', 'borrow_count', 'collection']


class CreateBorrowSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        book = validated_data.get('book')
        collection = get_object_or_404(Collection, pk=book.collection.pk)
        customer = validated_data.get('customer')

        if customer.is_ban:
            raise serializers.ValidationError({'customer': 'this is a ban customer'})

        if customer.balance < (collection.borrow_price * 3):
            raise serializers.ValidationError({'customer': 'customer balance is low.'})

        # check for book inventory
        if book.borrow_inventory == 0:
            raise serializers.ValidationError({'book': 'borrow inventory is low'})

        if Borrow.objects.filter(customer=customer, book__collection=collection).count() == collection.borrow_limit:
            raise serializers.ValidationError(f"customer brake the borrow limit rule for collection\
                 '{collection.title}({collection.borrow_limit})' .")

        expected_return_date = validated_data.get('expected_return_date')
        inventory = book.buy_inventory  # referred as n in the document
        today = datetime.datetime.today()
        last_30_days = today - datetime.timedelta(days=30)
        borrowed_in_last_30_days = Borrow.objects.filter(book=book,
                                                         borrow_date__lte=today,
                                                         borrow_date__gt=last_30_days
                                                         ).count()

        if borrowed_in_last_30_days < 3:
            borrowed_in_last_30_days = 3

        max_borrow_date = ((30 * inventory) // (inventory + borrowed_in_last_30_days)) + 1

        today = datetime.date.today()
        subtract = expected_return_date - today
        if subtract.days > max_borrow_date:
            raise serializers.ValidationError(
                {'expected_return_date': f'invalid return date(max return date {max_borrow_date})'})

        # update book inventory
        book.borrow_inventory -= 1
        book.save()
        return super().create(validated_data)

    class Meta:
        model = Borrow
        fields = ['id', 'book', 'customer', 'borrow_date', 'expected_return_date', 'actual_return_date']


class UpdateBorrowSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        customer = instance.customer
        customer_penalties = Penalties.objects.filter(borrow__customer=customer).count()
        if Penalties.objects.filter(borrow=instance).exists() and customer_penalties == 1:
            customer.is_ban = False
            customer.save()
        return super().update(instance, validated_data)

    class Meta:
        model = Borrow
        fields = ['actual_return_date']


class SimpleCustomerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Customer
        fields = ['id', 'user', 'balance', 'is_ban']


class BorrowListSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    customer = SimpleCustomerSerializer()

    class Meta:
        model = Borrow
        fields = ['id', 'customer', 'book', 'borrow_date', 'expected_return_date', 'actual_return_date']


class CustomerListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    borrow_set = BorrowListSerializer(many=True)
    borrow_count = serializers.IntegerField()

    class Meta:
        model = Customer
        fields = ['id', 'user', 'balance', 'is_ban', 'borrow_set', 'borrow_count']


class CustomerPenaltiesListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Customer
        fields = ['id', 'user', 'balance', 'is_ban', 'penalties_set']


class CreateBuySerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        customer = validated_data.get('customer')
        book = validated_data.get('book')
        if book.buy_inventory == 0:
            raise serializers.ValidationError({'book': 'buy inventory is low'})
        if customer.balance >= book.buy_price:
            customer.balance -= book.buy_price
            book.buy_inventory -= 1
            customer.save()
            book.save()
        else:
            raise serializers.ValidationError({"customer": 'customer inventory is low'})

        return super().create(validated_data)

    class Meta:
        model = Buy
        fields = ['id', 'customer', 'book', 'buy_date']
