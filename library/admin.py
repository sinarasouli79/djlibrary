from django.contrib import admin

from .models import Customer, Borrow, Librarian, Book, Collection, Penalties

# Register your models here.
admin.site.register(Customer)
admin.site.register(Borrow)
admin.site.register(Librarian)
admin.site.register(Book)
admin.site.register(Collection)
admin.site.register(Penalties)
