from django.urls import path

from library.views import CreateBorrow

urlpatterns = [
    path('borrow/', CreateBorrow.as_view())
]
