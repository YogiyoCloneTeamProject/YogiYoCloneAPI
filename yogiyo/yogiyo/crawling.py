import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from restaurants.models import Restaurant, MenuGroup


class Crawling:

    def bs(self, driver):
        """BeutifulSoup 로직 작성"""

    def selenium_js(self, driver):
        """JS 페이지 이동 로직"""
        y_position = 10000000
        scroll_cnt = 0
        for i in range(1):

            # 60개 크롤링 할 때 마다 scroll_cnt 증가
            if i % 60 == 0:
                scroll_cnt += 1
            if 9 < scroll_cnt:
                break

            # scroll_cnt 만큼 스크롤
            for j in range(scroll_cnt):
                time.sleep(1)
                driver.execute_script(f'window.scrollTo(0, {y_position});')

            time.sleep(3)
            driver.execute_script(
                f"""
                r_list = document.getElementsByClassName("item clearfix");
                // console.log(r_list.length);  // 첫 로딩 60개
                r_list[{i}].click();
                """
            )
            time.sleep(1)

            self.bs(driver)

            driver.execute_script('window.history.back();')  # 뒤로가기

    def crawl(self):
        driver = webdriver.Chrome('/Users/happy/Downloads/chromedriver')
        driver.implicitly_wait(3)
        url = 'https://www.yogiyo.co.kr/mobile/#/'
        driver.get(url)

        time.sleep(7)
        driver.execute_script('document.getElementsByClassName("btn btn-default ico-pick")[0].click();')
        self.selenium_js(driver)
        driver.close()


class CrawlingBS:
    driver = webdriver.Chrome('/Users/happy/Downloads/chromedriver')
    driver.implicitly_wait(3)
    url = 'https://www.yogiyo.co.kr/mobile/#/469716/'
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    name = soup.find('div', class_='restaurant-title').text.strip().replace('\n', '')
    star = soup.find('span', class_='stars star-point ng-binding').text.strip().replace('★', '').replace('\n', '')
    notification = soup.find('div', class_='info-text ng-binding').text.strip()

    info_1 = soup.find('div', class_='info-item-title info-icon1').parent
    key = info_1.find_all('i')
    val = info_1.find_all('span')
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
    for k, v in zip(key, val):
        k = k.text.strip()
        v = v.text.strip()
        if k == '상호명':
            business_name = v
        elif k == '사업자등록번호':
            company_registration_number = v

    info_4 = soup.find('div', class_='info-item-title info-icon4').parent
    origin_information = info_4.find('pre').text
    restaurant_list = []

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

    # food menu
    # menu_group_tags = soup.find_all('span', class_='menu-name pull-left ng-binding')
    menu_parent = soup.find_all('div', class_='panel panel-default ng-scope')
    menu_group_list = []
    for menu_group_div in menu_parent:
        menu_group_name = menu_group_div.find('span', class_='menu-name pull-left ng-binding')
        if menu_group_name is None or menu_group_name.text.strip() == 'Photo Menu Items' or '요기서결제' in menu_group_name.text:
            continue

        menu_group_name = menu_group_name.text.strip()

        # 메뉴 그룹 생성
        menu_group = MenuGroup(restaurant=restaurant, name=menu_group_name)
        menu_group.save()

        print(menu_group_div)

    driver.close()

# start_crawling = Crawling()
# start_crawling.crawl()
# crawling = CrawlingBS()