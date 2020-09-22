from rest_framework.routers import SimpleRouter

from orders.views import OrderViewSet
from restaurants.views import RestaurantViewSet, MenuViewSet
from reviews.views import ReviewViewSet
from users.views import UserViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'users', UserViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = router.urls
