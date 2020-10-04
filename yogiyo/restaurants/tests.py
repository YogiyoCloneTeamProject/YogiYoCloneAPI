import datetime

from django.test import TestCase
from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase

from restaurants.models import Restaurant


class RestaurantTestCase(APITestCase):
    def setUp(self) -> None:
        self.restaurants = baker.make('restaurants.Restaurant', _quantity=2,
                                      opening_time=datetime.time(hour=22, minute=30, second=0),
                                      average_rating=4, delivery_discount=1000, delivery_charge=2000,)
        self.restaurant = self.restaurants[0]
        self.user = baker.make('users.User')

    def test_restaurant_list(self):
        response = self.client.get('/restaurants')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for restaurant_response, restaurant in zip(response.data['results'], self.restaurants):
            self.assertEqual(restaurant_response['id'], restaurant.id)
            self.assertEqual(restaurant_response['name'], restaurant.name)
            self.assertEqual(restaurant_response['average_rating'], restaurant.average_rating)
            self.assertEqual(restaurant_response['image'], restaurant.image)
            self.assertEqual(restaurant_response['delivery_discount'], restaurant.delivery_discount)
            self.assertEqual(restaurant_response['delivery_charge'], restaurant.delivery_charge)

    def test_restaurant_detail(self):
        menu_group = baker.make('restaurants.MenuGroup', restaurant=self.restaurant)
        baker.make('restaurants.Menu', menu_group=menu_group)

        response = self.client.get(f'/restaurants/{self.restaurant.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_restaurant = Munch(response.data)
        self.assertEqual(response_restaurant.id, self.restaurant.id)
        self.assertEqual(response_restaurant.name, self.restaurant.name)
        self.assertEqual(response_restaurant.average_rating, self.restaurant.average_rating)
        self.assertEqual(response_restaurant.notification, self.restaurant.notification)
        self.assertEqual(response_restaurant.opening_time, self.restaurant.opening_time.strftime('%H:%M:%S'))
        self.assertEqual(response_restaurant.tel_number, self.restaurant.tel_number)
        self.assertEqual(response_restaurant.address, self.restaurant.address)
        self.assertEqual(response_restaurant.min_order_price, self.restaurant.min_order_price)
        self.assertEqual(response_restaurant.payment_methods, self.restaurant.payment_methods)
        self.assertEqual(response_restaurant.business_name, self.restaurant.business_name)
        self.assertEqual(response_restaurant.company_registration_number, self.restaurant.company_registration_number)
        self.assertEqual(response_restaurant.origin_information, self.restaurant.origin_information)
        self.assertEqual(response_restaurant.image, self.restaurant.image)
        self.assertEqual(response_restaurant.delivery_discount, self.restaurant.delivery_discount)
        self.assertEqual(response_restaurant.delivery_charge, self.restaurant.delivery_charge)

    def test_menu_detail(self):
        menu_group = baker.make('restaurants.MenuGroup', restaurant=self.restaurant)
        menu = baker.make('restaurants.Menu', menu_group=menu_group)
        option_group = baker.make('restaurants.OptionGroup', _quantity=2, menu=menu)
        options = []
        for i in range(len(option_group)):
            options.append(baker.make('restaurants.Option', option_group=option_group[i]))

        response = self.client.get(f'/menu/{menu.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        menu_response = Munch(response.data)
        self.assertEqual(menu_response.id, menu.id)
        self.assertEqual(menu_response.name, menu.name)
        # self.assertEqual(menu_response.image, menu.image)
        self.assertEqual(menu_response.caption, menu.caption)
        self.assertEqual(menu_response.price, menu.price)
        for optiongroup_response, optiongroup in zip(menu_response.option_group, option_group):
            self.assertEqual(optiongroup_response['id'], optiongroup.id)
            self.assertEqual(optiongroup_response['name'], optiongroup.name)
            self.assertEqual(optiongroup_response['menu_id'], optiongroup.menu_id)

            for option_res, opt in zip(optiongroup_response['option'], optiongroup.option.all()):
                self.assertEqual(option_res['id'], opt.id)
                self.assertEqual(option_res['name'], opt.name)
                self.assertEqual(option_res['price'], opt.price)
                self.assertEqual(option_res['option_group_id'], opt.option_group_id)

    def test_category_list(self):
        """카테고리 별 음식점 리스트 """
        self.restaurants[0].categories.extend(["중식", "피자"])
        self.restaurants[0].save()
        self.restaurants[1].categories.extend(["일식", "중식"])
        self.restaurants[1].save()

        category = "중식"
        response = self.client.get(f'/restaurants?categories={category}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        for r in response.data['results']:
            restaurant = Restaurant.objects.get(id=r['id'])
            self.assertTrue(category in restaurant.categories)

    def home_view_test(self, res):
        for restaurant_response in res:
            self.assertTrue('id' in restaurant_response)
            self.assertTrue('name' in restaurant_response)
            self.assertTrue('average_rating' in restaurant_response)
            self.assertTrue('image' in restaurant_response)
            self.assertTrue('delivery_discount' in restaurant_response)
            self.assertTrue('delivery_charge' in restaurant_response)
            self.assertTrue('delivery_time' in restaurant_response)
            self.assertTrue('bookmark_count' in restaurant_response)
            self.assertTrue('review_count' in restaurant_response)
            self.assertTrue('representative_menus' in restaurant_response)
            self.assertTrue('min_order_price' in restaurant_response)
            self.assertTrue('owner_comment_count' in restaurant_response)

    def test_home_view(self):
        for i in range(1, 10):
            response = self.client.get(f'/restaurants/home_view_{i}')
            res = response.data['results']
            self.assertEqual(response.status_code, status.HTTP_200_OK, res)
            if i == 4:
                self.assertTrue(len(res) <= 9)
            self.home_view_test(res)

    def test_post_tag_list(self):
        """태그 자동완성 list"""
        self.restaurant.tags.add("chicken", "pizza", "pasta", "coke", "pizza2")

        self.client.force_authenticate(user=self.user)
        search = "pi"
        response = self.client.get(f'/tags?name={search}')

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        for r in response.data:
            self.assertTrue(r['name'].startswith(search))
