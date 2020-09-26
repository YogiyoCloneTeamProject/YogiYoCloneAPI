from django.contrib.auth import authenticate
from rest_framework import serializers

from users.models import User, Bookmark, Profile


class UserPhoneNumSerializer(serializers.ModelSerializer):
    """회원가입2 전화번호 인증 (활성)"""
    phone_num = serializers.CharField(source='profile.phone_num')

    class Meta:
        model = User
        fields = ('id', 'email', 'nickname', 'phone_num')
        read_only_fields = ('email', 'nickname')


class UserUpdateSerializer(serializers.ModelSerializer):
    """회원정보 수정 - 닉네임, 전화번호 only"""
    phone_num = serializers.CharField(source='profile.phone_num')

    class Meta:
        model = User
        fields = ('id', 'email', 'nickname', 'phone_num')
        read_only_fields = ('email',)


class UserPasswordSerializer(serializers.ModelSerializer):
    """비밀번호 변경"""
    nickname = serializers.CharField(source='profile.nickname', allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'nickname', 'password',)
        read_only_fields = ('email', 'nickname')
        extra_kwargs = {'password': {'write_only': True}}


class UserCreateSerializer(serializers.ModelSerializer):
    """회원가입1 이메일, 비번, 닉네임 (비활)"""
    nickname = serializers.CharField(source='profile.nickname', allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'nickname')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        nickname = validated_data.pop('nickname') if 'nickname' in validated_data else None
        user = User.objects.create(**validated_data, is_active=False)
        Profile.objects.create(user=user, nickname=nickname)
        return user


class UserRetrieveSerializer(serializers.ModelSerializer):
    """유저 디테일"""
    nickname = serializers.CharField(source='profile.nickname', allow_null=True, allow_blank=True)
    phone_num = serializers.CharField(source='profile.phone_num', allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'nickname', 'phone_num')
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(serializers.Serializer):
    """로그인"""
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not (email and password):
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if user is None:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('id', 'restaurant')
