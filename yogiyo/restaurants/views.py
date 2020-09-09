from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from restaurants.models import Menu, Restaurant
from restaurants.serializers import RestaurantDetailSerializer, RestaurantListSerializer, MenuDetailSerializer
from rest_framework.exceptions import MethodNotAllowed


class MenuViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    """menu detail """
    queryset = Menu.objects.all()
    serializer_class = MenuDetailSerializer


class RestaurantViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """restaurant list, detail"""
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RestaurantDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        # query_params -> 카테고리
        if self.action == 'list':
            category = self.request.query_params.get('category', None)
            if category is not None:
                queryset = queryset.filter(categories__contains=[category])
        return queryset  # 카테고리 없으면 전체 조회
