from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase


class OrderCreateTestCase(APITestCase):
    """주문 생성"""

    def setUp(self) -> None:
        self.url = f'/orders'
        self.data = {
            "restaurant": 1,
            "order_menu": [
                {
                    "menu_id": "23",
                    "name": "불고기버거세트",
                    "count": "1",
                    "order_option_group": [
                        {
                            "name": "패티 추가",
                            "mandatory": "true",
                            "order_option": [
                                {
                                    "name": "소고기 패티",
                                    "price": "3000"
                                },
                                {
                                    "name": "불고기 패티",
                                    "price": "3000"
                                }
                            ]
                        },
                        # {
                        #     "name": "치즈 추가",
                        #     "option": {
                        #         "name": "모짜렐라치즈",
                        #         "price": "3000"
                        #     }
                        # }
                    ]
                },
                # {
                #     "menu_id": "24",
                #     "name": "치즈버거세트",
                #     "count": "1",
                #     "option_group": []
                # },
                # {
                #     "menu_id": "25",
                #     "name": "1994버거세트",
                #     "count": "1",
                #     "option_group": []
                # }
            ]
        }
        self.user = baker.make('users.User')
        self.user = baker.make('users.User')
        baker.make('users.Profile', user=self.user)

    def test_should_create(self):
        """생성-성공"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.data)
        res = response.data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, res)
        self.assertEqual(res['content'], self.data['content'])

        owner = res.get('owner')
        self.assertIsNotNone(owner)
        self.assertIsNotNone(owner.get('id'))
        self.assertIsNotNone(owner.get('nickname'))
