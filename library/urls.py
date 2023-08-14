from rest_framework.routers import DefaultRouter

from library.views import BorrowViewSet, CustomerListView, BuyCreateView

router = DefaultRouter()
router.register('borrow', BorrowViewSet, basename='borrow')
router.register('customer', CustomerListView, basename='book')
router.register('buy', BuyCreateView, basename='buy')
urlpatterns = router.urls
