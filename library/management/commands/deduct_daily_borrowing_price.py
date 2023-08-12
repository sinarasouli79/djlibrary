from django.core.management import BaseCommand

from library.models import Borrow


class Command(BaseCommand):
    help = 'deducting daily borrowing daily price from customer balance'

    def handle(self, *args, **options):
        borrows = Borrow.objects.select_related('customer').filter(actual_return_date__isnull=True)
        for borrow in borrows:
            customer = borrow.customer
            customer.balance -= borrow.book.collection.borrow_price
            customer.save()
