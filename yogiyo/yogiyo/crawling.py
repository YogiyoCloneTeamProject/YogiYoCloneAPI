import tempfile
import time

import requests
from bs4 import BeautifulSoup
from django.core import files
from rest_framework.utils import json
from selenium import webdriver

from restaurants.models import Restaurant, MenuGroup, Menu, OptionGroup, Option


class Crawling:

    def crawl(self):
        """모든 데이터 크롤링"""
        driver = webdriver.Chrome('/Users/joy/Downloads/chromedriver')
        driver.implicitly_wait(3)
        url = 'https://www.yogiyo.co.kr/mobile/#/'
        driver.get(url)

        time.sleep(7)
        driver.execute_script('document.getElementsByClassName("btn btn-default ico-pick")[0].click();')

        scroll_cnt = -1
        # 레스토랑 반복
        for i in range(10):
            # 60개 크롤링 할 때 마다 scroll_cnt 증가
            if i % 60 == 0:
                scroll_cnt += 1
            if 9 < scroll_cnt:
                break

            # scroll_cnt 만큼 스크롤
            for j in range(scroll_cnt):
                time.sleep(1)
                driver.execute_script(f'window.scrollTo(0, {100000000});')

            time.sleep(3)
            driver.execute_script(
                f"""
                r_list = document.getElementsByClassName("item clearfix");
                // console.log(r_list.length);  // 첫 로딩 60개
                r_list[{i}].click();
                """
            )
            time.sleep(1)
            self.crawl_page(driver)
            driver.execute_script('window.history.back();')  # 뒤로가기

        driver.close()

    def test_crawl(self):
        """테스트 10개만 크롤링"""
        driver = webdriver.Chrome('/Users/joy/Downloads/chromedriver')
        driver.implicitly_wait(3)
        page_id_list = [
            340303,
            445730,
            398257,
            229788,
            256308,
            229246,
            415433,
            330102,
            61406,
            322865
        ]
        driver.get('https://www.yogiyo.co.kr/mobile/#/340303/')
        time.sleep(2)

        for page_id in page_id_list:
            bs_url = f'https://www.yogiyo.co.kr/mobile/#/{page_id}/'
            driver.get(bs_url)
            time.sleep(3)
            self.crawl_page(driver)
        driver.close()

    def crawl_page(self, driver):
        """페이지 크롤링"""
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.find('div', class_='restaurant-title').text.strip().replace('\n', '')
        star = soup.find('span', class_='stars star-point ng-binding').text.strip().replace('★', '').replace('\n',
                                                                                                             '')
        notification = soup.find('div', class_='info-text ng-binding').text.strip()

        info_1 = soup.find('div', class_='info-item-title info-icon1').parent
        key = info_1.find_all('i')
        val = info_1.find_all('span')
        opening_hours = ''
        tel_number = ''
        address = ''
        for k, v in zip(key, val):
            k = k.text.strip()
            v = v.text.strip()
            if k == '영업시간':
                opening_hours = v
            elif k == '전화번호':
                tel_number = v
            elif k == '주소':
                address = v
            # elif k == '부가정보':
            #     company_registration_number = v

        info_2 = soup.find('div', class_='info-item-title info-icon2').parent
        key = info_2.find_all('i')
        val = info_2.find_all('span')
        min_order = ''
        payment_method = ''
        for k, v in zip(key, val):
            k = k.text.strip()
            v = v.text.strip()
            if k == '최소주문금액':
                min_order = v.replace('원', '').replace(',', '')
            elif k == '결제수단':
                payment_method = v

        info_3 = soup.find('div', class_='info-item-title info-icon3').parent
        key = info_3.find_all('i')
        val = info_3.find_all('span')
        business_name = ''
        company_registration_number = ''
        for k, v in zip(key, val):
            k = k.text.strip()
            v = v.text.strip()
            if k == '상호명':
                business_name = v
            elif k == '사업자등록번호':
                company_registration_number = v

        info_4 = soup.find('div', class_='info-item-title info-icon4').parent
        origin_information = info_4.find('pre').text

        restaurant_image = \
        soup.find('div', class_='restaurant-content').find('div', class_='logo').attrs['style'].split('"')[1]

        restaurant = Restaurant(
            name=name,
            star=star,
            notification=notification,
            opening_hours=opening_hours,
            tel_number=tel_number,
            address=address,
            min_order=min_order,
            payment_method=payment_method,
            business_name=business_name,
            company_registration_number=company_registration_number,
            origin_information=origin_information
        )
        restaurant.save()
        restaurant.image.save(*self.save_img('https://www.yogiyo.co.kr' + restaurant_image))

        # 식당 메뉴/ 옵션 크롤링
        s = requests.Session()
        s.headers.update({
            'x-apikey': 'iphoneap',
            'x-apisecret': 'fe5183cc3dea12bd0ce299cf110a75a2'
        })
        page_id = driver.current_url.split('/')[-2]
        api_url = f'https://www.yogiyo.co.kr/api/v1/restaurants/{page_id}/menu/?add_photo_menu=android&add_one_dish_menu=true&order_serving_type=delivery'
        r = s.get(api_url)
        response_str = r.content.decode('utf-8')
        menu_results = json.loads(response_str)
        self.menu_parsing(menu_results, restaurant)

    def menu_parsing(self, menu_results, restaurant):
        menu_results = menu_results[2:]
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
                    option_group = OptionGroup(menu=menu, name=option_group_name)
                    option_group.save()

                    for option_dict in option_group_dict['subchoices']:
                        option_name = option_dict['name']
                        option_price = option_dict['price']
                        option = Option(option_group=option_group, name=option_name, price=option_price)
                        option.save()

    def save_img(self, image_url):

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
