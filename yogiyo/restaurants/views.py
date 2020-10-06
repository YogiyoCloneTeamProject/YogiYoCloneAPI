from django.db.models import Q
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
    ordering_fields = ['average_rating', 'delivery_charge', 'min_order_price', 'delivery_time', 'review_count',
                       'owner_comment_count']
    ordering = ('id',)
    permission_classes = [AllowAny]
    HOME_VIEWS = ('home_view_1', 'home_view_2', 'home_view_3', 'home_view_4', 'home_view_5', 'home_view_6',
                  'home_view_7', 'home_view_8', 'home_view_9')
    HOME_VIEW_PAGE_SIZE = 20

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RestaurantDetailSerializer
        if self.action in self.HOME_VIEWS:
            return HomeViewSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = self.filter_by_distance_manual(qs)
        qs = self.filter_by_search(qs)

        return qs

    def filter_by_search(self, qs):
        search = self.request.query_params.get('search')
        if search:
            qs = Restaurant.objects.filter(Q(name__icontains=search) |
                                           Q(menu_group__menu__name__icontains=search) |
                                           Q(tags__name__icontains=search)).distinct()
        return qs

    def filter_by_distance_manual(self, qs):
        """좌표 기준 반경 1km 쿼리"""
        data = self.request.query_params
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

    @action(detail=False, methods=['GET'])
    def home_view_1(self, request, *args, **kwargs):
        """나의 입맛저격 - 별점 순"""
        qs = self.get_queryset().order_by('-average_rating').filter(average_rating__gte=4)
        return self.home_view_results(qs)

    @action(detail=False, methods=['GET'])
    def home_view_2(self, request, *args, **kwargs):
        """우리동네 찜 많은 음식점 - 찜 개수 순"""
        qs = self.get_queryset().order_by('-bookmark')
        return self.home_view_results(qs)

    @action(detail=False, methods=['GET'])
    def home_view_3(self, request, *args, **kwargs):
        """오늘만 할인 - 할인이 0원이 아닌 매장"""
        qs = self.get_queryset().filter(delivery_discount__gt=0)
        return self.home_view_results(qs)

    @action(detail=False, methods=['GET'])
    def home_view_4(self, request, *args, **kwargs):
        """요즘 뜨는 우리동네 음식점 - 9개만"""
        qs = self.get_queryset()[:9]
        return self.home_view_results(qs)

    @action(detail=False, methods=['GET'])
    def home_view_5(self, request, *args, **kwargs):
        """배달비 무료 - 배달비 0원"""
        qs = self.get_queryset().filter(delivery_charge=0)
        return self.home_view_results(qs)

    @action(detail=False, methods=['GET'])
    def home_view_6(self, request, *args, **kwargs):
        """최근 7일동안 리뷰가 많아요 - 리뷰 순"""
        qs = self.get_queryset().order_by('-review')
        return self.home_view_results(qs)

    @action(detail=False, methods=['GET'])
    def home_view_7(self, request, *args, **kwargs):
        """요기요 플러스 맛집"""
        qs = self.get_queryset()
        return self.home_view_results(qs)

    @action(detail=False, methods=['GET'])
    def home_view_8(self, request, *args, **kwargs):
        """가장 빨리 배달돼요"""
        qs = self.get_queryset().order_by('delivery_time')
        return self.home_view_results(qs)

    @action(detail=False, methods=['GET'])
    def home_view_9(self, request, *args, **kwargs):
        """새로 오픈했어요"""
        qs = self.get_queryset()
        return self.home_view_results(qs)

    def home_view_results(self, qs):
        serializer = self.get_serializer(qs[:self.HOME_VIEW_PAGE_SIZE], many=True)
        return Response({'results': serializer.data})


class TagViewSet(mixins.ListModelMixin, GenericViewSet):
    """tag - search (자동완성)"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = []
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_search = self.request.query_params.get('name')
        if tag_search:
            queryset = queryset.filter(name__icontains=tag_search)
        elif tag_search == '' or tag_search is None:
            queryset = []

        return queryset
