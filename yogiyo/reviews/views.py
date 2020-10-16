from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet

from core.permissions import IsSuperUser, IsOrderOwner, IsOwnerAndIsAuthenticated, IsOwner
from orders.models import Order
from reviews.models import Review, OwnerComment
from reviews.serializers import ReviewListSerializer, ReviewCreateSerializer, OwnerCommentSerializer


class ReviewCreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    리뷰 생성


    nested_url에 order_pk를 리뷰모델의 order_id에 저장
    req - taste, amount, delivery 의 평점 평균을 rating으로 저장
    order_pk로 오더 메뉴를 get하여 메뉴-옵션그룹-옵션을 menu_name으로 저장
    order의 owner와 req의 owner가 같은지 검증
    """
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsOrderOwner]

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


class ReviewListViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    리뷰 조회


    nested_url에서 restaurant_id로 레스토랑이 갖고 있는 리뷰 조회
    """
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        if 'restaurant_pk' in self.kwargs:
            return super().get_queryset().filter(restaurant=self.kwargs.get('restaurant_pk'))
        else:
            raise ValidationError('url should contains restaurant pk')


class ReviewDestroyViewSet(mixins.DestroyModelMixin, GenericViewSet):
    """
    리뷰 삭제


    토큰 필요
    """
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    permission_classes = [IsOwner]


class OwnerCommentViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = OwnerComment.objects.all()
    serializer_class = OwnerCommentSerializer
    permission_classes = [IsSuperUser]

    def partial_update(self, request, *args, **kwargs):
        """
        사장님 댓글 수정


        토큰 필요


        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        사장님 댓글 삭제


        토큰 필요
        """
        return super().destroy(request, *args, **kwargs)


class OwnerCommentCreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    사장님 댓글 생성


    nested_url에 review_pk를 오너코멘트모델의 review_id에 저장
    토큰 필요
    """
    queryset = OwnerComment.objects.all()
    serializer_class = OwnerCommentSerializer
    permission_classes = [IsSuperUser]

    def perform_create(self, serializer):
        if 'review_pk' in self.kwargs:
            review = get_object_or_404(Review, id=self.kwargs.get('review_pk'))
            serializer.save(review=review)
