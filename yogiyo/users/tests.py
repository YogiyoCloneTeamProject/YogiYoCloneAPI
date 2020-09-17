from model_bakery import baker
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import User

email = 'email@test.com'
password = '1234'


class UserRegisterTestCase(APITestCase):
    url = '/users'

    def test_should_create(self):
        data = {
            'email': email,
            'password': password,
        }
        response = self.client.post(self.url, data)
        res = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res['email'], email)

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


class UserLoginTestCase(APITestCase):
    url = '/users/login'

    def setUp(self) -> None:
        # self.user = baker.make(User, email=email, password=password)  # baker로 만들면 로그인 안됨..why
        self.user = User.objects.create(email=email, password=password)

    def test_with_correct_info(self):
        response = self.client.post(self.url, {'email': email, 'password': password})
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)
        self.assertTrue(Token.objects.filter(user=self.user, key=response.data['token']).exists())

    def test_without_password(self):
        response = self.client.post(self.url, {'email': email})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_wrong_password(self):
        response = self.client.post(self.url, {'email': email, 'password': '1111'})
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user_id=self.user.id).exists())

    # def test_should_denied_delete_token(self):
    #     response = self.client.delete(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertTrue(Token.objects.filter(user_id=self.user.id).exists())
