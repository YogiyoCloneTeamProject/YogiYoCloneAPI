from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from restaurants.models import Menu, Restaurant
from restaurants.serializers import RestaurantDetailSerializer, RestaurantListSerializer, MenuDetailSerializer


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
            if category:
                queryset = queryset.filter(categories__contains=[category])

            # query_params -> 위경도
            # lng = self.request.query_params.get('lng', None)
            # lat = self.request.query_params.get('lat', None)
            lng = 127.057129
            lat = 37.545133
            if lat and lng:
                queryset = queryset.filter(point__distance_lte=(Point(lng, lat), D(m=500)))

        return queryset  # 카테고리 없으면 전체 조회
