from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from users.models import User, Bookmark
from users.serializers import UserCreateSerializer, UserRetrieveSerializer, LoginSerializer, BookmarkSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
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
        return Response({"detail": "Successfully logged out."},
                        status=status.HTTP_200_OK)


class BookmarkViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    # todo 퍼미션 추가

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user:
            qs = qs.filter(user=self.request.user)
        # todo 비로그인시 400
        return qs
