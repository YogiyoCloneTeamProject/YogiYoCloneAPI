from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase


class OrderCreateTestCase(APITestCase):
    """주문 생성"""

    def setUp(self) -> None:
        self.restaurant = baker.make('restaurants.Restaurant')
        menu_group = baker.make('restaurants.MenuGroup', restaurant=self.restaurant, name='햄버거')
        self.menu = baker.make('restaurants.Menu', menu_group=menu_group, name='띠드버거')
        option_groups = []
        option_groups += baker.make('restaurants.OptionGroup', _quantity=1, name='움료추가', menu=self.menu)
        option_groups += baker.make('restaurants.OptionGroup', _quantity=1, name='패티추가', menu=self.menu)
        # option = []
        # for i in range(len(option_groups)):
        #     option += baker.make('restaurants.Option', _quantity=1, option_group=option_groups[i], name=f'option{i}')

        options = baker.make('restaurants.Option', _quantity=2, option_group=option_groups[0])

        self.url = f'/orders'
        self.data = {
            "restaurant": self.restaurant.id,
            "order_menu": [
                {
                    "menu": 1,
                    "name": self.menu.name,
                    "count": 1,
                    "price": self.menu.price,
                    "order_option_group": [
                        {
                            "name": option_groups[0].name,
                            "mandatory": "true",
                            "order_option": [
                                {
                                    "name": options[0].name,
                                    "price": options[0].price
                                },
                                {
                                    "name": options[1].name,
                                    "price": options[1].price
                                }
                            ]
                        },
                    ]
                },
            ]
        }
        self.user = baker.make('users.User')

    def test_should_create(self):
        """생성-성공"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.data)
        res = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, res)
        # print(res)
