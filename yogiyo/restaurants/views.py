from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from restaurants.models import Menu, Restaurant
from restaurants.serializers import RestaurantDetailSerializer, RestaurantListSerializer, MenuDetailSerializer


class MenuViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    """menu detail"""
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

            # PostGIS 거리 필터
            # queryset = self.filter_by_distance(queryset)

        return queryset  # 카테고리 없으면 전체 조회

    def filter_by_distance(self, qs):
        """query_params 위경도로 PointField 거리 필터링"""
        # 실제 query_params
        lng = self.request.query_params.get('lng', None)
        lat = self.request.query_params.get('lat', None)
        # 임의 좌표 사용
        # lng = 127.057129
        # lat = 37.545133

        if lat and lng:
            qs = qs.filter(point__distance_lte=(Point(lng, lat), D(m=500)))
        return qs

    @action(detail=False, methods=['GET'])
    def home_view_1(self, request, *args, **kwargs):
        """별점 - star 높은 음식점 10개 - 4점 이상만"""
        queryset = self.get_queryset().order_by('-star').filter(star__gte=4)[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def home_view_2(self, request, *args, **kwargs):
        """todo 우리동네 찜 많은 음식점"""
        queryset = self.get_queryset().order_by('-bookmark')[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def home_view_5(self, request, *args, **kwargs):
        """배달비 무료"""
        queryset = self.get_queryset().filter(delivery_charge=0)[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def home_view_6(self, request, *args, **kwargs):
        """todo 최근 7일동안 리뷰가 많아요
        - 리뷰 갯수 순 음식점 10개"""
        queryset = self.get_queryset().order_by('-review')[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
