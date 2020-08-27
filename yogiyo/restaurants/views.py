from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from restaurants.models import Menu, Restaurant
from restaurants.serializers import RestaurantDetailSerializer, RestaurantListSerializer, MenuListSerializer


class MenuViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuListSerializer


class RestaurantViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RestaurantDetailSerializer
        return super().get_serializer_class()
