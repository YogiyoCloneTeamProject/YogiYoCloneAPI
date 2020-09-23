from django.shortcuts import render
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet

from orders.models import Order
from reviews.models import Review
from reviews.serializers import ReviewListSerializer, ReviewCreateSerializer


class ReviewViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    """review"""
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer

    def get_serializer_class(self):
        if self.action == 'create':  # todo 딜리트는 나중에..!
            return ReviewCreateSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        if 'order_pk' in self.kwargs:
            order = get_object_or_404(Order, id=self.kwargs.get('order_pk'))
            rating = int((self.request.data['taste'] + self.request.data['delivery'] + self.request.data['amount']) / 3)

            # 메뉴 이름/count(옵션끄룹이름(옵션이름,옵션이름), 옵션그룹이름(옵션이름,옵션이름)), 메뉴2/count…
            menu_list = []
            for order_menu in order.order_menu.all():
                menu = order_menu.name + '/' + str(order_menu.count)
                order_option_group_list = []
                order_option_group = ''
                for order_option_group_obj in order_menu.order_option_group.all():
                    order_option_group += '(' + order_option_group_obj.name
                    for order_option_obj in order_option_group_obj.order_option.all():
                        order_option_group += '(' + order_option_obj.name + ')'
                    order_option_group += ')'
                    order_option_group_list.append(order_option_group)
                menu += ','.join(order_option_group_list)
                menu_list.append(menu)
            menu_name = ','.join(menu_list)

            serializer.save(
                owner=self.request.user,
                order=order,
                rating=rating,
                restaurant=order.restaurant,
                menu_name=menu_name
            )

    # def get_queryset(self):
    # queryset = super().get_queryset().filter(=self.kwargs.get('order_pk'))
    # return queryset
