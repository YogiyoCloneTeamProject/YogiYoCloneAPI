from django.test import TestCase
from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase


class RestaurantTestCase(APITestCase):
    def setUp(self) -> None:
        self.restaurants = baker.make('restaurants.Restaurant', _quantity=2)
        self.restaurant = self.restaurants[0]
        self.user = baker.make('users.User')

    def test_restaurant_list(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/restaurants')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for restaurant_response, restaurant in zip(response.data['results'], self.restaurants[::-1]):
            self.assertEqual(restaurant_response['id'], restaurant.id)
            self.assertEqual(restaurant_response['name'], restaurant.name)
            self.assertEqual(restaurant_response['star'], restaurant.star)
            self.assertEqual(restaurant_response['image'], restaurant.image)
            self.assertEqual(restaurant_response['delivery_discount'], restaurant.delivery_discount)
            self.assertEqual(restaurant_response['delivery_charge'], restaurant.delivery_charge)

    def test_restaurant_detail(self):
        menu_group = baker.make('restaurants.MenuGroup', _quantity=1, restaurant=self.restaurant)
        menu = baker.make('restaurants.Menu', _quantity=1, menu_group=menu_group[0])

        self.client.force_authenticate(user=self.user)

        response = self.client.get(f'/restaurants/{self.restaurant.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_restaurant = Munch(response.data)
        self.assertEqual(response_restaurant.id, self.restaurant.id)
        self.assertEqual(response_restaurant.name, self.restaurant.name)
        self.assertEqual(response_restaurant.star, self.restaurant.star)
        self.assertEqual(response_restaurant.notification, self.restaurant.notification)
        self.assertEqual(response_restaurant.opening_hours, self.restaurant.opening_hours)
        self.assertEqual(response_restaurant.tel_number, self.restaurant.tel_number)
        self.assertEqual(response_restaurant.address, self.restaurant.address)
        self.assertEqual(response_restaurant.min_order, self.restaurant.min_order)
        self.assertEqual(response_restaurant.payment_method, self.restaurant.payment_method)
        self.assertEqual(response_restaurant.business_name, self.restaurant.business_name)
        self.assertEqual(response_restaurant.company_registration_number, self.restaurant.company_registration_number)
        self.assertEqual(response_restaurant.origin_information, self.restaurant.origin_information)
        self.assertEqual(response_restaurant.image, self.restaurant.image)
        self.assertEqual(response_restaurant.delivery_discount, self.restaurant.delivery_discount)
        self.assertEqual(response_restaurant.delivery_charge, self.restaurant.delivery_charge)

    def test_menu_detail(self):
        menu_group = baker.make('restaurants.MenuGroup', _quantity=1, restaurant=self.restaurant)
        menu = baker.make('restaurants.Menu', _quantity=1, menu_group=menu_group[0])
        menu = menu[0]
        option_group = baker.make('restaurants.OptionGroup', _quantity=2, menu=menu)
        option = []
        for i in range(len(option_group)):
            option += baker.make('restaurants.Option', _quantity=1, option_group=option_group[i])
        self.client.force_authenticate(user=self.user)

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