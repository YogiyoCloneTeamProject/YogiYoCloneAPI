from rest_framework.routers import SimpleRouter

from orders.views import OrderViewSet
from restaurants.views import RestaurantViewSet, MenuViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = router.urls