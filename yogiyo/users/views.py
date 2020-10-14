from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.permissions import IsUserSelf
from restaurants.models import Restaurant
from restaurants.serializers import BookmarkRestaurantSerializer
from users.models import User, Bookmark
from users.serializers import UserCreateSerializer, UserRetrieveSerializer, LoginSerializer, BookmarkSerializer, \
    UserPhoneNumSerializer, UserPasswordSerializer, UserUpdateNicknameSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update_password', 'partial_update', 'logout', 'destroy']:
            return [IsUserSelf()]
        if self.action in ['login', 'authorize_phone_num', 'create', 'list']:
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserRetrieveSerializer
        if self.action == 'create':
            return UserCreateSerializer
        if self.action == 'authorize_phone_num':
            return UserPhoneNumSerializer
        if self.action == 'update_password':
            return UserPasswordSerializer
        if self.action == 'partial_update':
            return UserUpdateNicknameSerializer
        return super().get_serializer_class()

    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        """로그인"""
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=False)
    def logout(self, request, *args, **kwargs):
        """로그아웃"""
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True)
    def authorize_phone_num(self, request, *args, **kwargs):
        """회원가입2 전화번호 인증 후 - 전화번호 추가, 유저 활성화"""
        # todo 아무나 authorize_phone_num 할수없게 인증이 필요
        # todo create 후 전화번호 인증은 안했을때
        return super().partial_update(request, *args, **kwargs)

    @action(methods=['patch'], detail=True)
    def update_password(self, request, *args, **kwargs):
        """비밀번호 변경"""
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """회원 탈퇴(비활성화)"""
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_200_OK)


class BookmarkViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [AllowAny]


class BookmarkListViewSet(mixins.ListModelMixin,
                          GenericViewSet):
    # todo Restaurant -> Bookmark
    queryset = Restaurant.objects.all()
    serializer_class = BookmarkRestaurantSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            qs = qs.filter(bookmark__user=self.request.user)
        else:
            # todo 로그인 안한 유저의 찜 내역(테스트용) 삭제예정
            qs = qs.filter(bookmark__user=User.objects.first())
        return qs
