from django.urls import path
from rest_framework.routers import DefaultRouter

from library.views import BorrowViewSet, CustomerListView, BuyViewSet, report, BookViewSet, CollectionViewSet

router = DefaultRouter()
router.register('borrow', BorrowViewSet, basename='borrow')
router.register('customer', CustomerListView, basename='book')
router.register('buy', BuyViewSet, basename='buy')
router.register('book', BookViewSet, basename='book')
router.register('collection', CollectionViewSet, basename='collection')
urlpatterns = [
    path('report/', report, name='buy-profit-report')
]
urlpatterns += router.urls
