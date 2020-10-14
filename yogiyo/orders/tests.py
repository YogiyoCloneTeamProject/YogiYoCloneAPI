from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase

from orders.models import Order

INVALID_ID = -1


class OrderCreateTestCase(APITestCase):
    """주문 생성"""

    def setUp(self) -> None:
        self.restaurant = baker.make('restaurants.Restaurant', min_order_price=9000, delivery_discount=2000,
                                     delivery_charge=1000)
        menu_group = baker.make('restaurants.MenuGroup', restaurant=self.restaurant, name='햄버거')
        self.menu = baker.make('restaurants.Menu', menu_group=menu_group, name='띠드버거', price=9000)
        self.menu2 = baker.make('restaurants.Menu', menu_group=menu_group, name='불고기버', price=9000)
        self.option_groups = []
        self.option_groups += baker.make('restaurants.OptionGroup', _quantity=1, name='음료추가', mandatory=False,
                                         menu=self.menu)
        self.option_groups += baker.make('restaurants.OptionGroup', _quantity=1, name='패티추가', mandatory=True,
                                         menu=self.menu)
        self.option_groups_menu2 = baker.make('restaurants.OptionGroup', name='아무거나 추가', mandatory=True,
                                              menu=self.menu2)

        self.options = baker.make('restaurants.Option', _quantity=2, option_group=self.option_groups[0], price=1000)
        self.options2 = baker.make('restaurants.Option', _quantity=2, option_group=self.option_groups[1], price=500)

        self.url = '/orders'

        self.user = baker.make('users.User')

    def test_order_create(self):
        """생성-성공"""
        delivery_discount = self.restaurant.delivery_discount
        if delivery_discount is None:
            delivery_discount = 0
        data = {
            "restaurant": self.restaurant.id,
            "order_menu": [
                {
                    "menu": self.menu.id,
                    "name": self.menu.name,
                    "count": 1,
                    "price": self.menu.price,
                    "order_option_group": [
                        {
                            "name": self.option_groups[0].name,
                            "mandatory": False,
                            "order_option": [
                                {
                                    "name": self.options[0].name,
                                    "price": self.options[0].price
                                },
                                {
                                    "name": self.options[1].name,
                                    "price": self.options[1].price
                                }
                            ]
                        },
                        {
                            "name": self.option_groups[1].name,
                            "mandatory": True,
                            "order_option": [
                                {
                                    "name": self.options2[0].name,
                                    "price": self.options2[0].price
                                },
                            ]
                        },
                    ]
                },
            ],
            "address": "중림동",
            "delivery_requests": "소스 많이 주세요",
            "payment_method": Order.PaymentMethodChoice.CASH,
            "total_price": self.menu.price + self.options[0].price + self.options[1].price + self.options2[
                0].price + self.restaurant.delivery_charge - self.restaurant.delivery_discount
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data)
        response_order = Munch(response.data)
        data = Munch(data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for order_menu_obj, order_menu_req in zip(response_order.order_menu, data.order_menu):
            self.assertEqual(order_menu_obj['menu'], order_menu_req['menu'])
            self.assertEqual(order_menu_obj['name'], order_menu_req['name'])
            self.assertEqual(order_menu_obj['price'], order_menu_req['price'])
            self.assertEqual(order_menu_obj['count'], order_menu_req['count'])
            for order_option_group_obj, order_option_group_req in zip(order_menu_obj['order_option_group'], order_menu_req['order_option_group']):
                self.assertEqual(order_option_group_obj['name'], order_option_group_req['name'])
                self.assertEqual(order_option_group_obj['mandatory'], order_option_group_req['mandatory'])
                for order_option_obj, order_option_req in zip(order_option_group_obj['order_option'], order_option_group_req['order_option']):
                    self.assertEqual(order_option_obj['name'], order_option_req['name'])
                    self.assertEqual(order_option_obj['price'], order_option_req['price'])

        self.assertEqual(response_order.address, data.address)
        self.assertEqual(response_order.delivery_requests, data.delivery_requests)
        self.assertEqual(response_order.payment_method, data.payment_method)
        self.assertEqual(response_order.restaurant, data.restaurant)
        self.assertEqual(response_order.total_price, data.total_price)



    def test_order_create_menu_id(self):
        """req : menu.id -> wrong"""

        data = {
            "restaurant": self.restaurant.id,
            "order_menu": [
                {
                    "menu": INVALID_ID,  # here
                    "name": self.menu.name,
                    "count": 1,
                    "price": self.menu.price,
                    "order_option_group": [
                        {
                            "name": self.option_groups[0].name,
                            "mandatory": False,
                            "order_option": [
                                {
                                    "name": self.options[0].name,
                                    "price": self.options[0].price
                                },
                                {
                                    "name": self.options[1].name,
                                    "price": self.options[1].price
                                }
                            ]
                        },
                        {
                            "name": self.option_groups[1].name,
                            "mandatory": True,
                            "order_option": [
                                {
                                    "name": self.options2[0].name,
                                    "price": self.options2[0].price
                                },
                            ]
                        },
                    ]
                },
            ],
            "address": "중림동",
            "delivery_requests": "소스 많이 주세요",
            "payment_method": Order.PaymentMethodChoice.CASH,
            "total_price": self.menu.price + self.options[0].price + self.options[1].price + self.options2[
                0].price + self.restaurant.delivery_charge - self.restaurant.delivery_discount
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['order_menu'][0]['menu'][0], f'Invalid pk "{INVALID_ID}" - object does not exist.')

    def test_order_create_menu_name(self):
        """req : menu.name -> wrong"""

        data = {
            "restaurant": self.restaurant.id,
            "order_menu": [
                {
                    "menu": self.menu.id,
                    "name": '피자',  # here
                    "count": 1,
                    "price": self.menu.price,
                    "order_option_group": [
                        {
                            "name": self.option_groups[0].name,
                            "mandatory": False,
                            "order_option": [
                                {
                                    "name": self.options[0].name,
                                    "price": self.options[0].price
                                },
                                {
                                    "name": self.options[1].name,
                                    "price": self.options[1].price
                                }
                            ]
                        },
                        {
                            "name": self.option_groups[1].name,
                            "mandatory": True,
                            "order_option": [
                                {
                                    "name": self.options2[0].name,
                                    "price": self.options2[0].price
                                },
                            ]
                        },
                    ]
                },
            ],
            "address": "중림동",
            "delivery_requests": "소스 많이 주세요",
            "payment_method": Order.PaymentMethodChoice.CASH,
            "total_price": self.menu.price + self.options[0].price + self.options[1].price + self.options2[
                0].price + self.restaurant.delivery_charge - self.restaurant.delivery_discount
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'menu.name != model menu.name')

    def test_order_create_menu_price(self):
        """req : menu.price -> wrong"""

        data = {
            "restaurant": self.restaurant.id,
            "order_menu": [
                {
                    "menu": self.menu.id,
                    "name": self.menu.name,
                    "count": 1,
                    "price": 3000,  # here!
                    "order_option_group": [
                        {
                            "name": self.option_groups[0].name,
                            "mandatory": False,
                            "order_option": [
                                {
                                    "name": self.options[0].name,
                                    "price": self.options[0].price
                                },
                                {
                                    "name": self.options[1].name,
                                    "price": self.options[1].price
                                }
                            ]
                        },
                        {
                            "name": self.option_groups[1].name,
                            "mandatory": True,
                            "order_option": [
                                {
                                    "name": self.options2[0].name,
                                    "price": self.options2[0].price
                                },
                            ]
                        },
                    ]
                },
            ],
            "address": "중림동",
            "delivery_requests": "소스 많이 주세요",
            "payment_method": Order.PaymentMethodChoice.CASH,
            "total_price": self.menu.price + self.options[0].price + self.options[1].price + self.options2[
                0].price + self.restaurant.delivery_charge - self.restaurant.delivery_discount
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'menu.price != model menu.price')

    def test_order_create_order_option_group_name(self):
        """req : order_option_group.name -> wrong"""

        data = {
            "restaurant": self.restaurant.id,
            "order_menu": [
                {
                    "menu": self.menu.id,
                    "name": self.menu.name,
                    "count": 1,
                    "price": self.menu.price,
                    "order_option_group": [
                        {
                            "name": self.option_groups[0].name,
                            "mandatory": False,
                            "order_option": [
                                {
                                    "name": self.options[0].name,
                                    "price": self.options[0].price
                                },
                                {
                                    "name": self.options[1].name,
                                    "price": self.options[1].price
                                }
                            ]
                        },
                        {
                            "name": "맛잇는 옵션!",  # here! self.option_groups[1].name
                            "mandatory": True,
                            "order_option": [
                                {
                                    "name": self.options2[0].name,
                                    "price": self.options2[0].price
                                },
                            ]
                        },
                    ]
                },
            ],
            "address": "중림동",
            "delivery_requests": "소스 많이 주세요",
            "payment_method": Order.PaymentMethodChoice.CASH,
            "total_price": self.menu.price + self.options[0].price + self.options[1].price + self.options2[
                0].price + self.restaurant.delivery_charge - self.restaurant.delivery_discount
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'This option group is not included in this menu')

    def test_order_create_order_option_group_mandatory(self):
        """req : order_option_group.mandatory -> wrong"""

        data = {
            "restaurant": self.restaurant.id,
            "order_menu": [
                {
                    "menu": self.menu.id,
                    "name": self.menu.name,
                    "count": 1,
                    "price": self.menu.price,
                    "order_option_group": [
                        {
                            "name": self.option_groups[0].name,
                            "mandatory": False,
                            "order_option": [
                                {
                                    "name": self.options[0].name,
                                    "price": self.options[0].price
                                },
                                {
                                    "name": self.options[1].name,
                                    "price": self.options[1].price
                                }
                            ]
                        },
                        {
                            "name": self.option_groups[1].name,
                            "mandatory": False,  # here!
                            "order_option": [
                                {
                                    "name": self.options2[0].name,
                                    "price": self.options2[0].price
                                },
                            ]
                        },
                    ]
                },
            ],
            "address": "중림동",
            "delivery_requests": "소스 많이 주세요",
            "payment_method": Order.PaymentMethodChoice.CASH,
            "total_price": self.menu.price + self.options[0].price + self.options[1].price + self.options2[
                0].price + self.restaurant.delivery_charge - self.restaurant.delivery_discount
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0],
                         'order_option_group.mandatory != model option_group.mandatory')

    def test_order_create_order_option_group_mandatory_option_len(self):
        """req : order_option_group.mandatory true -> len(option) != 1"""

        data = {
            "restaurant": self.restaurant.id,
            "order_menu": [
                {
                    "menu": self.menu.id,
                    "name": self.menu.name,
                    "count": 1,
                    "price": self.menu.price,
                    "order_option_group": [
                        {
                            "name": self.option_groups[0].name,
                            "mandatory": False,
                            "order_option": [
                                {
                                    "name": self.options[0].name,
                                    "price": self.options[0].price
                                },
                                {
                                    "name": self.options[1].name,
                                    "price": self.options[1].price
                                }
                            ]
                        },
                        {
                            "name": self.option_groups[1].name,
                            "mandatory": True,
                            "order_option": [
                                {
                                    "name": self.options2[0].name,
                                    "price": self.options2[0].price
                                },
                                {  # here!
                                    "name": self.options2[0].name,
                                    "price": self.options2[0].price
                                }
                            ]
                        },
                    ]
                },
            ],
            "address": "중림동",
            "delivery_requests": "소스 많이 주세요",
            "payment_method": Order.PaymentMethodChoice.CASH,
            "total_price": self.menu.price + self.options[0].price + self.options[1].price + self.options2[
                0].price + self.restaurant.delivery_charge - self.restaurant.delivery_discount
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'mandatory true -> must len(order option list) == 1')

    def test_order_create_order_option_name(self):
        """req : order_option name  -> wrong"""

        data = {
            "restaurant": self.restaurant.id,
            "order_menu": [
                {
                    "menu": self.menu.id,
                    "name": self.menu.name,
                    "count": 1,
                    "price": self.menu.price,
                    "order_option_group": [
                        {
                            "name": self.option_groups[0].name,
                            "mandatory": False,
                            "order_option": [
                                {
                                    "name": self.options[0].name,
                                    "price": self.options[0].price
                                },
                                {
                                    "name": self.options[1].name,
                                    "price": self.options[1].price
                                }
                            ]
                        },
                        {
                            "name": self.option_groups[1].name,
                            "mandatory": True,
                            "order_option": [
                                {
                                    "name": "sj",  # here!
                                    "price": self.options2[0].price
                                },
                            ]
                        },
                    ]
                },
            ],
            "address": "중림동",
            "delivery_requests": "소스 많이 주세요",
            "payment_method": Order.PaymentMethodChoice.CASH,
            "total_price": self.menu.price + self.options[0].price + self.options[1].price + self.options2[
                0].price + self.restaurant.delivery_charge - self.restaurant.delivery_discount
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'This option is not included in this option group')

    def test_order_create_order_option_price(self):
        """req : order_option price  -> wrong"""

        data = {
            "restaurant": self.restaurant.id,
            "order_menu": [
                {
                    "menu": self.menu.id,
                    "name": self.menu.name,
                    "count": 1,
                    "price": self.menu.price,
                    "order_option_group": [
                        {
                            "name": self.option_groups[0].name,
                            "mandatory": False,
                            "order_option": [
                                {
                                    "name": self.options[0].name,
                                    "price": self.options[0].price
                                },
                                {
                                    "name": self.options[1].name,
                                    "price": self.options[1].price
                                }
                            ]
                        },
                        {
                            "name": self.option_groups[1].name,
                            "mandatory": True,
                            "order_option": [
                                {
                                    "name": self.options2[0].name,
                                    "price": 4000  # here!
                                },
                            ]
                        },
                    ]
                },
            ],
            "address": "중림동",
            "delivery_requests": "소스 많이 주세요",
            "payment_method": Order.PaymentMethodChoice.CASH,
            "total_price": self.menu.price + self.options[0].price + self.options[1].price + self.options2[
                0].price + self.restaurant.delivery_charge - self.restaurant.delivery_discount
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'order option.price != model option.price')

    def test_order_create_order_min_order_price(self):
        """req : total price < restaurant min price"""

        data = {
            "restaurant": self.restaurant.id,
            "order_menu": [
                {
                    "menu": self.menu.id,
                    "name": self.menu.name,
                    "count": 1,
                    "price": self.menu.price,
                    "order_option_group": [
                        {
                            "name": self.option_groups[0].name,
                            "mandatory": False,
                            "order_option": [
                                {
                                    "name": self.options[0].name,
                                    "price": self.options[0].price
                                },
                                {
                                    "name": self.options[1].name,
                                    "price": self.options[1].price
                                }
                            ]
                        },
                        {
                            "name": self.option_groups[1].name,
                            "mandatory": True,
                            "order_option": [
                                {
                                    "name": self.options2[0].name,
                                    "price": self.options2[0].price
                                },
                            ]
                        },
                    ]
                },
            ],
            "address": "중림동",
            "delivery_requests": "소스 많이 주세요",
            "payment_method": Order.PaymentMethodChoice.CASH,
            "total_price": 8000
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'total price < restaurant min price')

    def test_order_create_order_total_price(self):
        """req : total price -> wrong"""

        data = {
            "restaurant": self.restaurant.id,
            "order_menu": [
                {
                    "menu": self.menu.id,
                    "name": self.menu.name,
                    "count": 1,
                    "price": self.menu.price,
                    "order_option_group": [
                        {
                            "name": self.option_groups[0].name,
                            "mandatory": False,
                            "order_option": [
                                {
                                    "name": self.options[0].name,
                                    "price": self.options[0].price
                                },
                                {
                                    "name": self.options[1].name,
                                    "price": self.options[1].price
                                }
                            ]
                        },
                        {
                            "name": self.option_groups[1].name,
                            "mandatory": True,
                            "order_option": [
                                {
                                    "name": self.options2[0].name,
                                    "price": self.options2[0].price
                                },
                            ]
                        },
                    ]
                },
            ],
            "address": "중림동",
            "delivery_requests": "소스 많이 주세요",
            "payment_method": Order.PaymentMethodChoice.CASH,
            "total_price": 12000
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'total price != check_price')

    def test_menu_count(self):
        pass


class OrderListTestCase(APITestCase):
    """주문 내역 리스트"""

    def setUp(self) -> None:
        self.restaurant = baker.make('restaurants.Restaurant', min_order_price=10000)
        menu_group = baker.make('restaurants.MenuGroup', restaurant=self.restaurant, name='햄버거')
        self.menu = baker.make('restaurants.Menu', menu_group=menu_group, name='띠드버거', price=9000)
        self.menu2 = baker.make('restaurants.Menu', menu_group=menu_group, name='불고기버', price=9000)
        self.option_groups = []
        self.option_groups += baker.make('restaurants.OptionGroup', _quantity=1, name='음료추가', mandatory=False,
                                         menu=self.menu)
        self.option_groups += baker.make('restaurants.OptionGroup', _quantity=1, name='패티추가', mandatory=True,
                                         menu=self.menu)
        self.option_groups_menu2 = baker.make('restaurants.OptionGroup', name='아무거나 추가', mandatory=True,
                                              menu=self.menu2)

        self.options = baker.make('restaurants.Option', _quantity=2, option_group=self.option_groups[0], price=1000)
        self.options2 = baker.make('restaurants.Option', _quantity=2, option_group=self.option_groups[1], price=500)
        self.orders = baker.make('orders.Order', _quantity=2)
        self.url = '/orders'

        self.user = baker.make('users.User')

    def test_order_list(self):
        pass
        # response = self.client.get(self.url)
        #
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        #
