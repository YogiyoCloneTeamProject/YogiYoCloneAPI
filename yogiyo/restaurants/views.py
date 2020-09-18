# from django.contrib.gis.geos import Point
# from django.contrib.gis.measure import D
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.paginations import Pagination
from restaurants.models import Menu, Restaurant
from restaurants.serializers import RestaurantDetailSerializer, RestaurantListSerializer, MenuDetailSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter


class MenuViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    """menu detail"""
    queryset = Menu.objects.all()
    serializer_class = MenuDetailSerializer


class RestaurantFilter(filters.FilterSet):
    payment_methods = filters.CharFilter(lookup_expr='icontains')
    categories = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Restaurant
        fields = ['payment_methods', 'categories']


class RestaurantViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """restaurant list, detail"""
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantListSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = RestaurantFilter
    ordering_fields = ['star', 'delivery_charge', 'min_order_price', 'review_count']
    ordering = ('id',)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RestaurantDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        # PostGIS 거리 필터
        queryset = self.filter_by_distance_manual(queryset)
        return queryset  # 카테고리 없으면 전체 조회

    # def filter_by_distance_GIS(self, qs):
    #     """query_params 위경도로 PointField 거리 필터링"""
    #     # 실제 query_params
    #     lng = self.request.query_params.get('lng', None)
    #     lat = self.request.query_params.get('lat', None)
    #     # 임의 좌표 사용
    #     # lng = 127.057129
    #     # lat = 37.545133
    #
    #     if lat and lng:
    #         qs = qs.filter(point__distance_lte=(Point(lng, lat), D(m=500)))
    #     return qs

    def filter_by_distance_manual(self, qs):
        data = self.request.GET
        if self.action == 'list':
            lat = data.get('lat')
            lng = data.get('lng')
            if lat and lng:
                lat = float(lat)
                lng = float(lng)
                min_lat = lat - 0.0045
                max_lat = lat + 0.0045
                min_lon = lng - 0.007
                max_lon = lng + 0.007

                # 최소, 최대 위경도를 1km씩 설정해서 쿼리
                qs = qs.filter(lat__gte=min_lat, lat__lte=max_lat,
                               lng__gte=min_lon, lng__lte=max_lon)
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
