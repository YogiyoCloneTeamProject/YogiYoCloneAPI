import random
import tempfile
from datetime import datetime
from uuid import uuid4

import requests
from django.conf import settings
from django.core import files
from rest_framework.utils import json

from orders.models import Order
from restaurants.models import Restaurant, MenuGroup, Menu, OptionGroup, Option
from reviews.models import Review, ReviewComment, ReviewImage
from users.models import User

lat = 37.545133
lng = 127.057129


class Crawling:

    def __init__(self) -> None:
        settings.CRAWLING = True

        self.s = requests.Session()
        self.s.headers.update({
            'x-apikey': 'iphoneap',
            'x-apisecret': 'fe5183cc3dea12bd0ce299cf110a75a2'
        })

    def create_users(self):
        for i in range(1, 4):
            User(email=f'{uuid4()}testuser@a.com', password='1111').save()
        return list(User.objects.all())

    def json_parsing(self):
        """yogiyo_data_for_parsing.json 파일에서 파싱헤서 DB에 저장"""
        with open('yogiyo_data_for_parsing.json', 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        user_list = self.create_users()

        for restaurant_data in json_data:
            restaurant_results = restaurant_data['restaurant_results']
            restaurant_info_results = restaurant_data['restaurant_info_results']
            list_info = restaurant_data['list_info']
            review_results = restaurant_data['review_results']
            menu_results = restaurant_data['menu_results']
            avgrating_results = restaurant_data['avgrating_results']

            restaurant = self.restaurant_parsing(restaurant_results, restaurant_info_results, list_info,
                                                 avgrating_results)
            self.review_parsing(review_results, restaurant, user_list=user_list)
            self.menu_parsing(menu_results, restaurant)

    def json_crawl(self):
        """웹에서 크롤 -> yogiyo_data_for_parsing.json 파일로 저장"""
        list_info_dict = self.get_page_id_list()
        self.dict_to_json_file(list_info_dict)

    def restaurant_parsing(self, restaurant_results, restaurant_info_results, list_info, avgrating_results):
        # top - info
        name = restaurant_results['name']
        min_order = restaurant_results['min_order_amount']
        methods = []
        for method in restaurant_results['payment_methods']:
            if method == "creditcard":
                methods.append("신용카드")
                methods.append("현금")
            elif method == "online":
                methods.append("요기서결제")

        payment_methods = methods
        try:
            discount = restaurant_results['discounts']['additional']['delivery']['amount']
        except KeyError:
            discount = 0
        delivery_charge = restaurant_results.get('delivery_fee')
        res_lat = restaurant_results['lat']
        res_lng = restaurant_results['lng']
        restaurant_image = restaurant_results['logo_url']
        restaurant_back_image = restaurant_results['background_url']
        categories = restaurant_results['categories']

        # bottom - info
        notification = restaurant_info_results['introduction_by_owner'].get('introduction_text') \
            if restaurant_info_results.get('introduction_by_owner') else ''
        s = restaurant_info_results['opening_time_description'].split(' - ')
        opening_time = datetime.strptime(s[0], '%H:%M')
        closing_time = datetime.strptime(s[1], '%H:%M')
        tel_number = restaurant_info_results['phone']
        address = restaurant_info_results['address']
        business_name = restaurant_info_results['crmdata']['company_name']
        company_registration_number = restaurant_info_results['crmdata']['company_number']
        origin_information = restaurant_info_results['country_origin']

        representative_menus = list_info['representative_menus']

        average = avgrating_results['average']
        average_delivery = avgrating_results['average_delivery']
        average_quantity = avgrating_results['average_quantity']
        average_taste = avgrating_results['average_taste']

        try:
            estimated_delivery_time = int(restaurant_results['estimated_delivery_time'].split('~')[0])
        except:
            estimated_delivery_time = 30

        restaurant = Restaurant(
            name=name,
            notification=notification,
            opening_time=opening_time,
            closing_time=closing_time,
            tel_number=tel_number,
            address=address,
            min_order_price=min_order,  # 20분~30분 - 20~30분
            payment_methods=payment_methods,
            business_name=business_name,
            company_registration_number=company_registration_number,
            origin_information=origin_information,
            delivery_discount=discount,
            delivery_charge=delivery_charge,
            delivery_time=estimated_delivery_time,
            lat=res_lat,
            lng=res_lng,
            categories=categories,

            representative_menus=representative_menus,

            # 평균 평점
            average_rating=average,
            average_taste=average_taste,
            average_delivery=average_delivery,
            average_amount=average_quantity,
        )
        restaurant.save()
        if restaurant_image:
            restaurant.image.save(*self.save_img('https://www.yogiyo.co.kr' + restaurant_image))
        if restaurant_back_image:
            restaurant.back_image.save(*self.save_img(restaurant_back_image))
        return restaurant

    def review_parsing(self, review_results, restaurant, user_list):

        for i in range(5):
            try:
                review_dict = review_results[i]
            except IndexError:
                break
            owner = random.choice(user_list)
            order = Order.objects.create(restaurant=restaurant, owner=owner, address='as',
                                         payment_method=Order.PaymentMethodChoice.CASH, total_price=1000,
                                         status=Order.OrderStatusChoice.DELIVERY_COMPLETE)
            review = Review(
                owner=owner,
                restaurant=restaurant,
                order=order,
                menu_name=review_dict['menu_summary'][:100],
                rating=review_dict['rating'],
                taste=review_dict['rating_taste'],
                delivery=review_dict['rating_delivery'],
                amount=review_dict['rating_quantity'],
                caption=review_dict['comment'][:298],
                like_count=review_dict['like_count'],
            )
            review.save()
            for img in review_dict['review_images']:
                review_image = ReviewImage(review=review)
                review_image.image.save(*self.save_img(img['thumb']))

            owner_reply = review_dict['owner_reply']
            if owner_reply:
                review_comment = ReviewComment(
                    review=review,
                    comments=owner_reply['comment'],
                )
                review_comment.save()

    def menu_parsing(self, menu_results, restaurant):
        """json에서 '메뉴그룹, 메뉴, 옵션그룹, 옵션' 파싱"""
        photo_menu_items = []
        for menu_group_dict in menu_results:
            menu_group_name = menu_group_dict['name']
            # 포토메뉴리스트에 메뉴 이름 저장
            if menu_group_dict['slug'] == 'photo_menu_items':
                photo_menu_items = [item['name'] for item in menu_group_dict['items']]
                continue

            # 탑텐, 인기메뉴, 요기서 결제 시 할인 = 스킵
            if menu_group_dict['slug'] in ('top_items', 'additional_discount_items'):
                continue

            menu_group = MenuGroup(
                restaurant=restaurant,
                name=menu_group_name,
            )
            menu_group.save()

            for menu_dict in menu_group_dict['items']:
                menu_name = menu_dict['name']
                # 메뉴이름이 포토메뉴리스트에 있다면 True
                menu_is_photomenu = True if menu_name in photo_menu_items else False
                menu_price = int(menu_dict['price'])
                menu_img = menu_dict.get('image')
                menu_caption = menu_dict.get('description')
                menu = Menu(name=menu_name, menu_group=menu_group, price=menu_price,
                            caption=menu_caption, is_photomenu=menu_is_photomenu)
                menu.save()
                if menu_img is not None:
                    menu.image.save(*self.save_img(menu_img))
                for option_group_dict in menu_dict['subchoices']:
                    option_group_name = option_group_dict['name']
                    option_group_mandatory = option_group_dict['mandatory']
                    option_group = OptionGroup(menu=menu, name=option_group_name, mandatory=option_group_mandatory)
                    option_group.save()

                    option_list = []
                    for option_dict in option_group_dict['subchoices']:
                        option_name = option_dict['name']
                        option_price = option_dict['price']
                        option_list.append(Option(option_group=option_group, name=option_name, price=option_price))
                    Option.objects.bulk_create(option_list)

    def save_img(self, image_url):
        """이미지 저장"""
        request = requests.get(image_url, stream=True)
        if request.status_code != requests.codes.ok:
            return

        file_name = image_url.split('/')[-1].split('?')[0]
        lf = tempfile.NamedTemporaryFile()

        for block in request.iter_content(1024 * 8):
            if not block:
                break
            lf.write(block)

        return file_name, files.File(lf)

    def dict_to_json_file(self, list_info_dict):
        crawl_data = []
        for page_id in list_info_dict.keys():
            restaurant_api_url = f'https://www.yogiyo.co.kr/api/v1/restaurants/{page_id}/?lat={lat}&lng={lng}'
            restaurant_info_api_url = f'https://www.yogiyo.co.kr/api/v1/restaurants/{page_id}/info/'
            review_api_url = f'https://www.yogiyo.co.kr/api/v1/reviews/{page_id}/?count=30&only_photo_review=false&page=1&sort=time'
            menu_api_url = f'https://www.yogiyo.co.kr/api/v1/restaurants/{page_id}/menu/?add_photo_menu=android&add_one_dish_menu=true&order_serving_type=delivery'
            avgrating_url = f'https://www.yogiyo.co.kr/review/restaurant/{page_id}/avgrating/'

            restaurant_data = {
                'list_info': list_info_dict[page_id],
                'restaurant_results': self.get_response_json_data(restaurant_api_url),
                'restaurant_info_results': self.get_response_json_data(restaurant_info_api_url),
                'review_results': self.get_response_json_data(review_api_url),
                'menu_results': self.get_response_json_data(menu_api_url),
                'avgrating_results': self.get_response_json_data(avgrating_url),
            }
            crawl_data.append(restaurant_data)

        with open('yogiyo_data_for_parsing.json', 'w', encoding='utf-8') as file:
            json.dump(crawl_data, file, ensure_ascii=False, indent='\t')

    def get_response_json_data(self, url):
        """API URL -> JSON -> 딕셔너리"""
        r = self.s.get(url)
        response_str = r.content.decode('utf-8')
        return json.loads(response_str)

    def get_page_id_list(self):
        """레스토랑 id 리스트"""
        restaurant_list_url = f'https://www.yogiyo.co.kr/api/v1/restaurants-geo/?items=60&lat={lat}&lng={lng}&order=rank&page=0&search='
        restaurant_list_results = self.get_response_json_data(restaurant_list_url)['restaurants']

        list_info_dict = {restaurant_dict['id']: restaurant_dict for restaurant_dict in restaurant_list_results}

        return list_info_dict
