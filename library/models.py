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

    def __str__(self):
        return self.title


class Librarian(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=5, decimal_places=2)
    is_ban = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.first_name}-{self.user.last_name}'


class Borrow(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)

    # def clean_expected_return_date(self, expected_return_date):
    #     subtract = expected_return_date - self.borrow_date
    #     if subtract.days < 0:
    #         raise models.ValidationError('invalid return date(return date should be after borrow date)')
    #
    #     return expected_return_date


class Penalties(models.Model):
    date = models.DateField(auto_now_add=True)
    customer = models.OneToOneField(Customer, on_delete=models.PROTECT)
    borrow = models.OneToOneField(Borrow, on_delete=models.PROTECT)
