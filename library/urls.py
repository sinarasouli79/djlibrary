from rest_framework.routers import DefaultRouter

from library.views import BorrowViewSet, CustomerListView

router = DefaultRouter()
router.register('borrow', BorrowViewSet, basename='borrow')
router.register('customer', CustomerListView, basename='book')
urlpatterns = router.urls
