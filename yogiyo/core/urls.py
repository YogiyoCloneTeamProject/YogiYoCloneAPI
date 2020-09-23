from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from orders.views import OrderViewSet
from restaurants.views import RestaurantViewSet, MenuViewSet
from reviews.views import ReviewViewSet
from users.views import UserViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'users', UserViewSet)
# router.register(r'reviews', ReviewViewSet)

review_router = routers.NestedSimpleRouter(router, r'orders', lookup='order')
review_router.register(r'reviews', ReviewViewSet, basename='order_review')

urlpatterns = router.urls + review_router.urls
