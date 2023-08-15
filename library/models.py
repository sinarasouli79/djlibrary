from decimal import Decimal

from django.conf import settings
from django.db import models


# Create your models here.

class Collection(models.Model):
    title = models.CharField(max_length=255)
    borrow_price = models.DecimalField(max_digits=5, decimal_places=2)
    borrow_limit = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=255)
    borrow_inventory = models.PositiveIntegerField()
    buy_inventory = models.PositiveIntegerField()
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    buy_price = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.0))

    def __str__(self):
        return self.title


class Librarian(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=5, decimal_places=2)
    is_ban = models.BooleanField(default=False)


class Borrow(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)


class Penalties(models.Model):
    date = models.DateField(auto_now_add=True)
    borrow = models.ForeignKey(Borrow, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(10.00))


class Buy(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    buy_date = models.DateField(auto_now_add=True)
