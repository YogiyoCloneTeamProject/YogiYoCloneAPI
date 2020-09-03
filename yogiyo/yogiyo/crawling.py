import tempfile
import time

import requests
from bs4 import BeautifulSoup
from django.core import files
from rest_framework.utils import json
from selenium import webdriver

from restaurants.models import Restaurant, MenuGroup, Menu, OptionGroup, Option
from reviews.models import Review, ReviewImage

lat = 37.545133
lng = 127.057129


class Crawling:

    def __init__(self) -> None:
        self.s = requests.Session()
        self.s.headers.update({
            'x-apikey': 'iphoneap',
            'x-apisecret': 'fe5183cc3dea12bd0ce299cf110a75a2'
        })

    def get_response_json_data(self, url):
        """API URL -> JSON -> 딕셔너리"""
        r = self.s.get(url)
        response_str = r.content.decode('utf-8')
        return json.loads(response_str)

    def real_crawl(self):
        restaurant_list_url = f'https://www.yogiyo.co.kr/api/v1/restaurants-geo/?items=200&lat={37.545133}&lng={127.057129}&order=rank&page=0&search='
        restaurant_list_results = self.get_response_json_data(restaurant_list_url)

        page_id_list = [restaurant_dict['id'] for restaurant_dict in restaurant_list_results['restaurants']]
        # self.save_crawling_data_to_json(page_id_list)
        for page_id in page_id_list:
            self.api_parsing(page_id)

    def test_crawl(self):
        """테스트 10개만 크롤링"""
        page_id_list = [
            340303,
            445730,
            398257,
            229788,
            256308,
            229246,
            415433,
            330102,
            320025,
            322865
        ]
        for page_id in page_id_list:
            self.api_parsing(page_id)

    def api_parsing(self, page_id):
        restaurant_api_url = f'https://www.yogiyo.co.kr/api/v1/restaurants/{page_id}/?lat={lat}&lng={lng}'
        restaurant_info_api_url = f'https://www.yogiyo.co.kr/api/v1/restaurants/{page_id}/info/'
        review_api_url = f'https://www.yogiyo.co.kr/api/v1/reviews/{page_id}/?count=30&only_photo_review=false&page=1&sort=time'

        restaurant_results = self.get_response_json_data(restaurant_api_url)
        restaurant_info_results = self.get_response_json_data(restaurant_info_api_url)
        review_results = self.get_response_json_data(review_api_url)

    def review_parsing(self, review_results, restaurant):
        for review_dict in review_results:
            review = Review(
                # owner=user,
                restaurant=restaurant,
                # order=,
                rating=review_dict['rating'],
                taste=review_dict['rating_taste'],
                delivery=review_dict['rating_delivery'],
                amount=review_dict['rating_quantity'],
                caption=review_dict['comment'],
            )
            review.save()
            for img in review_dict['review_images']:
                review_image = ReviewImage(review=review)
                review_image.image.save(*self.save_img('https://www.yogiyo.co.kr' + img))

    def menu_parsing(self, menu_results, restaurant):
        """json에서 '메뉴그룹, 메뉴, 옵션그룹, 옵션' 파싱"""
        # todo 포토 메뉴 파싱 필요
        menu_results = menu_results[2:]  # todo 포토 메뉴, 탑텐, 인기메뉴 스킵
        for menu_group_dict in menu_results:
            menu_group_name = menu_group_dict['name']
            menu_group = MenuGroup(
                restaurant=restaurant,
                name=menu_group_name,
            )
            menu_group.save()

            for menu_dict in menu_group_dict['items']:
                menu_name = menu_dict['name']
                menu_price = int(menu_dict['price'])
                menu_img = menu_dict.get('image')
                menu_caption = menu_dict.get('description')
                menu = Menu(name=menu_name, menu_group=menu_group, price=menu_price, caption=menu_caption)
                menu.save()
                if menu_img is not None:
                    menu.image.save(*self.save_img(menu_img))
                for option_group_dict in menu_dict['subchoices']:
                    option_group_name = option_group_dict['name']
                    option_group_mandatory = option_group_dict['mandatory']
                    option_group = OptionGroup(menu=menu, name=option_group_name, mandatory=option_group_mandatory)
                    option_group.save()

                    for option_dict in option_group_dict['subchoices']:
                        option_name = option_dict['name']
                        option_price = option_dict['price']
                        option = Option(option_group=option_group, name=option_name, price=option_price)
                        option.save()

    def save_img(self, image_url):
        """이미지 저장"""
        # Steam the image from the url
        request = requests.get(image_url, stream=True)

        # Was the request OK?
        if request.status_code != requests.codes.ok:
            return

        # Get the filename from the url, used for saving later
        file_name = image_url.split('/')[-1].split('?')[0]

        # Create a temporary file
        lf = tempfile.NamedTemporaryFile()

        # Read the streamed image in sections
        for block in request.iter_content(1024 * 8):

            # If no more file then stop
            if not block:
                break

            # Write image block to temporary file
            lf.write(block)

        # Create the model you want to save the image to

        # Save the temporary image to the model#
        # This saves the model so be sure that is it valid
        return file_name, files.File(lf)

    def save_crawling_data_to_json(self, page_id_list):
        crawl_data = []
        for page_id in page_id_list:
            restaurant_api_url = f'https://www.yogiyo.co.kr/api/v1/restaurants/{page_id}/?lat={lat}&lng={lng}'
            restaurant_info_api_url = f'https://www.yogiyo.co.kr/api/v1/restaurants/{page_id}/info/'
            review_api_url = f'https://www.yogiyo.co.kr/api/v1/reviews/{page_id}/?count=30&only_photo_review=false&page=1&sort=time'
            menu_api_url = f'https://www.yogiyo.co.kr/api/v1/restaurants/{page_id}/menu/?add_photo_menu=android&add_one_dish_menu=true&order_serving_type=delivery'

            restaurant_data = {
                'restaurant_results': self.get_response_json_data(restaurant_api_url),
                'restaurant_info_results': self.get_response_json_data(restaurant_info_api_url),
                'review_results': self.get_response_json_data(review_api_url),
                'menu_results': self.get_response_json_data(menu_api_url),
            }
            crawl_data.append(restaurant_data)
        self.to_json(crawl_data)

    def to_json(self, crawl_data):
        with open('yogiyo_crawl.json', 'w', encoding='utf-8') as file:
            json.dump(crawl_data, file, ensure_ascii=False, indent='\t')
