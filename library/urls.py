from django.urls import path
from rest_framework.routers import DefaultRouter

from library.views import BorrowViewSet, CustomerViewSet, BuyViewSet, report, BookViewSet, CollectionViewSet

router = DefaultRouter()
router.register('borrow', BorrowViewSet, basename='borrow')
router.register('customer', CustomerViewSet, basename='customer')
router.register('buy', BuyViewSet, basename='buy')
router.register('book', BookViewSet, basename='book')
router.register('collection', CollectionViewSet, basename='collection')
urlpatterns = [
    path('report/', report, name='buy-profit-report')
]
urlpatterns += router.urls
