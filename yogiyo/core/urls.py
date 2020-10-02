from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from orders.views import OrderViewSet
from restaurants.views import RestaurantViewSet, MenuViewSet, TagViewSet
from reviews.views import ReviewViewSet, ReviewCreateViewSet
from restaurants.views import RestaurantViewSet, MenuViewSet
from reviews.views import ReviewViewSet, ReviewCreateViewSet, OwnerCommentViewSet
from users.views import UserViewSet, BookmarkListViewSet, BookmarkViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'users', UserViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'bookmarks', BookmarkListViewSet)
# router.register(r'bookmarks', BookmarkViewSet)
router.register(r'tags', TagViewSet)

""" review create """
review_router = routers.NestedSimpleRouter(router, r'orders', lookup='order')
review_router.register(r'reviews', ReviewCreateViewSet, basename='order_review')
""" review list """
review_list_router = routers.NestedSimpleRouter(router, r'restaurants', lookup='restaurant')
review_list_router.register(r'reviews', ReviewViewSet, basename='restaurant_review')
"""review_comment create"""
review_comment_router = routers.NestedSimpleRouter(router, r'reviews', lookup='review')
review_comment_router.register(r'comment', OwnerCommentViewSet, basename='review_comment')

urlpatterns = router.urls + review_router.urls + review_list_router.urls +review_comment_router.urls
