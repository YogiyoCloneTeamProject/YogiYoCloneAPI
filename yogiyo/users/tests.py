from model_bakery import baker
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import User, Profile

email = 'email@test.com'
password = '1111'
nickname = 'nickname'


class UserRegisterTestCase(APITestCase):
    url = '/users'

    def test_should_create(self):
        data = {
            'email': email,
            'password': password,
            'nickname': None
        }
        response = self.client.post(self.url, data)
        res = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, res)
        self.assertEqual(res['email'], data['email'])
        self.assertEqual(res['nickname'], data['nickname'])
        self.assertFalse(User.objects.get(id=res['id']).is_active)

    def test_without_email(self):
        response = self.client.post(self.url, {'email': '', 'password': password})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_format(self):
        wrong_email = 'wrong@format'
        response = self.client.post(self.url, {'email': wrong_email, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_without_password(self):
        response = self.client.post(self.url, {'email': email, 'password': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_duplicated_email(self):
        duplicated_email = 'duplicated_email@test.com'
        self.user = baker.make(User, email=duplicated_email, password=password)
        response = self.client.post(self.url, {'email': duplicated_email, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserRetrieveTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = baker.make('users.User')
        baker.make('users.Profile', user=self.user)

    def test_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/users/{self.user.id}')

        res = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK, res)
        self.assertEqual(self.user.profile.nickname, res['nickname'])
        self.assertEqual(self.user.profile.phone_num, res['phone_num'])
        self.assertEqual(self.user.email, res['email'])


class UserAuthorizePhoneNumTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = baker.make('users.User', is_active=False)
        baker.make('users.Profile', user=self.user)
        self.data = {
            'phone_num': '010-1111-1111'
        }

    def test_success(self):
        response = self.client.patch(f'/users/{self.user.id}/authorize_phone_num', data=self.data)

        res = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK, res)
        authorizde_user = User.objects.get(id=res['id'])
        self.assertEqual(self.data['phone_num'], res['phone_num'])
        self.assertEqual(authorizde_user.profile.phone_num, res['phone_num'])
        self.assertTrue(authorizde_user.is_active)
        self.assertEqual(self.user.email, res['email'])
        self.assertEqual(self.user.profile.nickname, res['nickname'])


class UserUpdatePasswordTestCase(APITestCase):

    def setUp(self) -> None:
        self.old_password = '1111'
        self.new_password = '2222'
        self.user = baker.make('users.User', email=email, password=self.old_password)
        baker.make('users.Profile', user=self.user)
        self.data = {'password': self.new_password}

    def test_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/users/{self.user.id}/update_password', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        response = self.client.post('/users/login', {'email': email, 'password': self.new_password})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)


class UserLoginTestCase(APITestCase):
    url = '/users/login'

    def setUp(self) -> None:
        self.user = baker.make('users.User', email=email, password=password)

    def test_with_correct_info(self):
        response = self.client.post(self.url, {'email': email, 'password': password})
        res = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, res)
        self.assertTrue('token' in res)
        self.assertTrue(Token.objects.filter(user=self.user, key=res['token']).exists())

    def test_without_password(self):
        response = self.client.post(self.url, {'email': email})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_wrong_password(self):
        response = self.client.post(self.url, {'email': email, 'password': '4444'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_without_email(self):
        response = self.client.post(self.url, {'password': password})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_wrong_email(self):
        response = self.client.post(self.url, {'email': 'wrong@email.com', 'password': password})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLogoutTestCase(APITestCase):
    url = '/users/logout'

    def setUp(self) -> None:
        self.user = baker.make(User, email=email, password=password)
        self.token = baker.make(Token, user=self.user)

    def test_should_delete_token(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertFalse(Token.objects.filter(user_id=self.user.id).exists())

    # def test_should_denied_delete_token(self):
    #     response = self.client.delete(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertTrue(Token.objects.filter(user_id=self.user.id).exists())
