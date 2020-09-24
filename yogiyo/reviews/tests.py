from django.test import TestCase
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from core.temporary_image import TempraryImageMixin
from orders.models import Order
from restaurants.models import Restaurant


class ReviewTestCase(APITestCase, TempraryImageMixin):
    def setUp(self) -> None:
        self.user = baker.make('users.User')
        self.restaurant = baker.make('restaurants.Restaurant', review_count=10, amount=4, delivery=4, taste=4, rating=4)
        self.order = baker.make('orders.Order', owner=self.user, restaurant=self.restaurant)
        self.order_menu = baker.make('orders.OrderMenu', order=self.order, name='불고기버거')
        self.order_menu2 = baker.make('orders.OrderMenu', order=self.order, name='치즈버거')
        self.order_option_group = baker.make('orders.OrderOptionGroup', order_menu=self.order_menu, name='치즈추가')
        self.order_option_group2 = baker.make('orders.OrderOptionGroup', order_menu=self.order_menu2, name='콜라추가')
        self.order_option = baker.make('orders.OrderOption', order_option_group=self.order_option_group, name='치즈 많이')
        self.order_option1 = baker.make('orders.OrderOption', order_option_group=self.order_option_group, name='치즈 조금')
        self.order_option2 = baker.make('orders.OrderOption', order_option_group=self.order_option_group2, name='콜라 많이')
        self.order_option2_1 = baker.make('orders.OrderOption', order_option_group=self.order_option_group2,
                                          name='콜라 쪼금')

    def test_review_create(self):
        self.data = {
            "caption": "jmt!!",
            "taste": 3,
            "delivery": 4,
            "amount": 2,
            "img": []
        }
        self.client.force_authenticate(user=self.user)

        response = self.client.post(f'/orders/{self.order.id}/reviews', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response)
        self.assertTrue(Order.objects.get(id=self.order.id).review_written)

    def test_review_create_img(self):
        image_test = [self.temporary_image(), self.temporary_image()]

        self.data = {
            "caption": "jmt!!",
            "taste": 3,
            "delivery": 4,
            "amount": 2,
            "img": image_test
        }
        self.client.force_authenticate(user=self.user)

        response = self.client.post(f'/orders/{self.order.id}/reviews', data=self.data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response)
        self.assertEqual(len(response.data['_img']), len(image_test))

    def test_review_duplicate(self):
        self.data = {
            "caption": "jmt!!",
            "taste": 3,
            "delivery": 4,
            "amount": 2,
        }
        self.client.force_authenticate(user=self.user)

        baker.make('reviews.Review', order=self.order)
        response = self.client.post(f'/orders/{self.order.id}/reviews', data=self.data)

        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_destroy(self):
        review = baker.make('reviews.Review', order=self.order)

        response = self.client.delete(f'/reviews/{review.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_review_list(self):
        baker.make('reviews.Review', restaurant=self.restaurant, _quantity=2)
        baker.make('reviews.Review')
        response = self.client.get(f'/restaurants/{self.restaurant.id}/reviews')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_star_restaurant(self):
        """리뷰에서 준 별점들이 해당 레스토랑에 값 반영 """
        self.data = {
            "caption": "jmt!!",
            "taste": 3,
            "delivery": 4,
            "amount": 2,
            "img" :[]
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.post(f'/orders/{self.order.id}/reviews', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response)

        saved_restaurant = Restaurant.objects.get(id=self.restaurant.id)

        # 현재 평균 = 원래 평균 * 원래 리뷰수 + 리퀘스트 / 총 리뷰 수
        self.assertEqual(saved_restaurant.taste, (self.restaurant.taste * self.restaurant.review_count + self.data[
            'taste']) / saved_restaurant.review_count)
        self.assertEqual(saved_restaurant.delivery, (
                self.restaurant.delivery * self.restaurant.review_count + self.data[
            'delivery']) / saved_restaurant.review_count)
        self.assertEqual(saved_restaurant.amount, (self.restaurant.amount * self.restaurant.review_count + self.data[
            'amount']) / saved_restaurant.review_count)
