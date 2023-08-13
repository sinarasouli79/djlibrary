from rest_framework.routers import DefaultRouter

from library.views import BorrowViewSet

router = DefaultRouter()
router.register('borrow', BorrowViewSet, basename='borrow')
urlpatterns = router.urls
