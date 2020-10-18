from django.contrib.auth import authenticate
from rest_framework import serializers

from users.models import User, Bookmark, Profile


class UserPhoneNumSerializer(serializers.ModelSerializer):
    """회원가입2 전화번호 인증 (활성)"""
    phone_num = serializers.CharField(source='profile.phone_num')
    nickname = serializers.CharField(source='profile.nickname', allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'nickname', 'phone_num')
        read_only_fields = ('email', 'nickname')
        examples = {
            "id": 16,
            "email": "testt@email.com",
            "nickname": "1111",
            "phone_num": "010-1111-2222"
        }

    def update(self, instance, validated_data):
        instance.profile.phone_num = validated_data.pop('profile')['phone_num']
        instance.profile.save()
        instance.is_active = True
        instance.save()
        return instance


class UserUpdateNicknameSerializer(serializers.ModelSerializer):
    """회원정보 수정 - 닉네임 only"""
    phone_num = serializers.CharField(source='profile.phone_num', read_only=True)
    nickname = serializers.CharField(source='profile.nickname', allow_null=True, allow_blank=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'nickname', 'phone_num')
        read_only_fields = ('email',)
        examples = {
            "id": 16,
            "email": "testt@email.com",
            "nickname": "1111",
            "phone_num": "010-1111-2222"
        }

    def update(self, user, validated_data):
        user.profile.nickname = validated_data.pop('profile').get('nickname')
        user.profile.save()
        return user


class UserPasswordSerializer(serializers.ModelSerializer):
    """비밀번호 변경"""
    nickname = serializers.CharField(source='profile.nickname', allow_null=True, allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'nickname', 'password')
        read_only_fields = ('email', 'nickname')
        extra_kwargs = {'password': {'write_only': True}}
        examples = {
            "id": 12,
            "email": "nbnnnb@email.com",
            "nickname": "postman"
        }

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    """회원가입1 이메일, 비번, 닉네임 (비활)"""
    nickname = serializers.CharField(source='profile.nickname', allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'nickname')
        extra_kwargs = {'password': {'write_only': True}}
        examples = {
            "id": 18,
            "email": "b@a.com",
            "nickname": "joy"
        }

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        user = User.objects.create(**validated_data, is_active=False)
        Profile.objects.create(user=user, **profile)
        return user


class UserRetrieveSerializer(serializers.ModelSerializer):
    """유저 디테일"""
    nickname = serializers.CharField(source='profile.nickname', allow_null=True, allow_blank=True)
    phone_num = serializers.CharField(source='profile.phone_num', allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'nickname', 'phone_num')
        extra_kwargs = {'password': {'write_only': True}}
        examples = {
            "id": 16,
            "email": "testt@email.com",
            "nickname": "1111",
            "phone_num": "010-1111-2222"
        }


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

    class Meta:
        examples = {
            "token": "09f236368ed266b5ccaf58e88b0618d573032f16",
            "user_id": 1
        }


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('id', 'user', 'restaurant')
        examples = {
            "id": 3,
            "name": "1인찜닭삼계탕전문&단물곤물-건대점",
            "average_rating": 4.8,
            "image": "https://yogiyo-s3.s3.ap-northeast-2.amazonaws.com/media/restaurant_image/%EC%B0%9C%EB%8B%AD10_20131128_FoodAD_crop_200x200_7byHP1N_RDEE6t4.jpg",
            "back_image": "https://yogiyo-s3.s3.ap-northeast-2.amazonaws.com/media/restaurant_back_image/20190624143217474693_8e592b8516e9b16906e2425bcf9a28d0_tn_YSZBpFE.jpg",
            "delivery_discount": 0,
            "delivery_charge": 2500,
            "delivery_time": "50~60분",
            "review_count": 5,
            "representative_menus": "（혼밥강추!）1人 삼계탕, （혼밥강추!）1.5人 순살찜닭 반마리",
            "owner_comment_count": 1
        }
