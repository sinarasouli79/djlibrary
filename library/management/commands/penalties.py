import datetime

from django.core.management import BaseCommand

from library.models import Borrow, Penalties


class Command(BaseCommand):
    help = "deducting daily penalties price from customers that didn't return the book"

    def handle(self, *args, **options):
        today = datetime.date.today()
        borrows = Borrow.objects.select_related('customer').filter(actual_return_date__isnull=True,
                                                                   expected_return_date__lt=today)
        for borrow in borrows:
            customer = borrow.customer
            if not Penalties.objects.filter(borrow=borrow).exists():
                customer.is_ban = True
                penalty = Penalties.objects.create(borrow=borrow)
                customer.balance -= penalty.price
                customer.save()
