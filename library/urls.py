from django.urls import path
from rest_framework.routers import DefaultRouter

from library.views import BorrowViewSet, CustomerListView, BuyCreateView, report, BookViewSet

router = DefaultRouter()
router.register('borrow', BorrowViewSet, basename='borrow')
router.register('customer', CustomerListView, basename='book')
router.register('buy', BuyCreateView, basename='buy')
router.register('book', BookViewSet, basename='book')
urlpatterns = [
    path('report/', report, name='buy-profit-report')
]
urlpatterns += router.urls
