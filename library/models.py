from django.conf import settings
from django.db import models


# Create your models here.

class Collection(models.Model):
    title = models.CharField(max_length=255)
    borrow_price = models.DecimalField(max_digits=5, decimal_places=2)
    borrow_limit = models.PositiveIntegerField()


class Book(models.Model):
    title = models.CharField(max_length=255)
    borrow_inventory = models.PositiveIntegerField()
    buy_inventory = models.PositiveIntegerField()
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)


class Librarian(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=5, decimal_places=2)
    is_ban = models.BooleanField(default=False)


class Borrow(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.PROTECT)
    book = models.OneToOneField(Book, on_delete=models.PROTECT)
    borrow_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True, blank=True)


class Penalties(models.Model):
    date = models.DateField(auto_now_add=True)
    customer = models.OneToOneField(Customer, on_delete=models.PROTECT)
    borrow = models.OneToOneField(Borrow, on_delete=models.PROTECT)
