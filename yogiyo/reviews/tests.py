from django.test import TestCase
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase


class ReviewTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = baker.make('users.User')
        self.restaurant = baker.make('restaurants.Restaurant')
        self.order = baker.make('orders.Order', owner=self.user, restaurant=self.restaurant)

    def test_review_create(self):
        self.data = {
            "caption": "jmt!!",
            "taste": 3,
            "delivery": 4,
            "amount": 2,
            "order_menu" : "asas",
            "restaurant" : self.restaurant.id
        }
        # 시리얼라이저 400 에러 추가.... . . . .ㅎr..
        self.client.force_authenticate(user=self.user)

        response = self.client.post(f'/orders/{self.order.id}/reviews', data=self.data)
        response = self.client.post(f'/orders/{self.order.id}/reviews', data=self.data)

        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response)
