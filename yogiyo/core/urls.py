from rest_framework.routers import SimpleRouter

from restaurants.views import RestaurantViewSet, MenuViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'restaurants', RestaurantViewSet)

router.register(r'menu', MenuViewSet)

urlpatterns = router.urls
