from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet

from core.permissions import IsSuperUser
from orders.models import Order
from reviews.models import Review, OwnerComment
from reviews.serializers import ReviewListSerializer, ReviewCreateSerializer, OwnerCommentSerializer


class ReviewCreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    """review post """
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    # permission_classes = [IsOrderOwner] # todo 퍼미션
    permission_classes = []

    def perform_create(self, serializer):
        if 'order_pk' in self.kwargs:
            order = get_object_or_404(Order, id=self.kwargs.get('order_pk'))
            rating = (int(self.request.data['taste']) + int(self.request.data['delivery']) + int(
                self.request.data['amount'])) / 3

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


class ReviewViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    """review get, delete"""
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            if 'restaurant_pk' in self.kwargs:
                queryset = super().get_queryset().filter(restaurant=self.kwargs.get('restaurant_pk'))
            else:
                raise ValidationError('url should contains restaurant pk ')
        return queryset


class OwnerCommentViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = OwnerComment.objects.all()
    serializer_class = OwnerCommentSerializer
    permission_classes = [IsSuperUser]


class OwnerCommentCreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = OwnerComment.objects.all()
    serializer_class = OwnerCommentSerializer
    permission_classes = [IsSuperUser]

    def perform_create(self, serializer):
        if 'review_pk' in self.kwargs:
            review = get_object_or_404(Review, id=self.kwargs.get('review_pk'))
            serializer.save(review=review)
