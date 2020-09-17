from rest_framework.routers import SimpleRouter

from orders.views import OrderViewSet
from restaurants.views import RestaurantViewSet, MenuViewSet
from users.views import UserViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls
