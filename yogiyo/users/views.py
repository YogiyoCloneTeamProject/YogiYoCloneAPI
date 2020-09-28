from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from core.permissions import IsUserSelf
from users.models import User, Bookmark
from users.serializers import UserCreateSerializer, UserRetrieveSerializer, LoginSerializer, BookmarkSerializer, \
    UserPhoneNumSerializer, UserPasswordSerializer, UserUpdateSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ['retrieve', 'update_password', 'partial_update', 'logout']:
            return [IsUserSelf()]
        if self.action in ['login', 'authorize_phone_num', 'create', 'list']:
            return []
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
            return UserUpdateSerializer
        return super().get_serializer_class()

    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=False)
    def logout(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True)
    def authorize_phone_num(self, request, *args, **kwargs):
        """회원가입2 전화번호 인증 후 - 전화번호 추가, 유저 활성화"""
        return super().partial_update(request, *args, **kwargs)

    @action(methods=['patch'], detail=True)
    def update_password(self, request, *args, **kwargs):
        """비밀번호 변경"""
        return super().partial_update(request, *args, **kwargs)


class BookmarkViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user:
            qs = qs.filter(user=self.request.user)
        return qs
