from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.db.models import Q
from taggit.models import Tag

from restaurants.models import Menu, Restaurant
from restaurants.serializers import RestaurantDetailSerializer, RestaurantListSerializer, MenuDetailSerializer, \
    HomeViewSerializer, TagSerializer

HOME_VIEWS = ('home_view_1', 'home_view_2', 'home_view_3', 'home_view_4', 'home_view_5', 'home_view_6')


class MenuViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    """menu detail"""
    queryset = Menu.objects.all()
    serializer_class = MenuDetailSerializer
    permission_classes = []


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
    ordering_fields = ['average_rating', 'delivery_charge', 'min_order_price', 'review_count', 'delivery_time']
    ordering = ('id',)
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RestaurantDetailSerializer
        if self.action in HOME_VIEWS:
            return HomeViewSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_by_distance_manual(queryset)

        search = self.request.query_params.get('search', None)
        if search:
            queryset = Restaurant.objects.filter(
                Q(name__icontains=search) | Q(menu_group__menu__name__icontains=search)).distinct()
        return queryset

    def filter_by_distance_manual(self, qs):
        """좌표 기준 반경 1km 쿼리"""
        data = self.request.GET
        if self.action == 'list':
            lat = data.get('lat')
            lng = data.get('lng')
            if lat and lng:
                lat = float(lat)
                lng = float(lng)
                min_lat = lat - 0.009
                max_lat = lat + 0.009
                min_lon = lng - 0.015
                max_lon = lng + 0.01

                # 최소, 최대 위경도를 1km씩 설정해서 쿼리
                qs = qs.filter(lat__gte=min_lat, lat__lte=max_lat,
                               lng__gte=min_lon, lng__lte=max_lon)
        return qs

    # todo 우리 동네만
    @action(detail=False, methods=['GET'])
    def home_view_1(self, request, *args, **kwargs):
        """별점 - star 높은 음식점 10개 - 4점 이상만"""
        queryset = self.get_queryset().order_by('-average_rating').filter(average_rating__gte=4)[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def home_view_2(self, request, *args, **kwargs):
        """todo 우리동네 찜 많은 음식점"""
        queryset = self.get_queryset().order_by('-bookmark')[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def home_view_3(self, request, *args, **kwargs):
        """배달비 무료"""
        queryset = self.get_queryset().filter(delivery_charge=0)[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def home_view_4(self, request, *args, **kwargs):
        """최근 7일동안 리뷰가 많아요
        - 리뷰 개수 순 음식점 10개"""
        queryset = self.get_queryset().order_by('-review')[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def home_view_5(self, request, *args, **kwargs):
        """todo 가장 빨리 배달돼요
        - 배달예상시간 순"""
        queryset = self.get_queryset().order_by('delivery_time')[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TagViewSet(mixins.ListModelMixin, GenericViewSet):
    """tag - search (자동완성)"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = []
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_search = self.request.query_params.get('name', None)
        if tag_search is not None:
            queryset = queryset.filter(name__icontains=tag_search)
        return queryset
