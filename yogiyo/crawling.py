import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class Crawling:

    def bs(self, driver):
        """BeutifulSoup 로직 작성"""
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

    def click_restaurant(self, driver, i):
        time.sleep(3)
        driver.execute_script(
            f"""
            r_list = document.getElementsByClassName("item clearfix");
            r_list[{i}].click();
            """
        )
        time.sleep(1)

    def selenium_js(self, driver):
        """JS 페이지 이동 로직"""
        y_position = 100000000
        scroll_cnt = 0
        for i in range(1000):

            # 60개 크롤링 할 때 마다 scroll_cnt 증가
            if i != 0 and i % 60 == 0:
                scroll_cnt += 1
            if 9 < scroll_cnt:
                break

            # scroll_cnt 만큼 스크롤
            for j in range(scroll_cnt):
                time.sleep(1)
                driver.execute_script(f'window.scrollTo(0, {y_position});')

            # 음식점 페이지로 이동
            self.click_restaurant(driver, i)

            # 뷰티풀수프 크롤링
            self.bs(driver)

            # 뒤로가기
            driver.execute_script('window.history.back();')

    def crawl(self):
        driver = webdriver.Chrome('/Users/joy/Downloads/chromedriver')
        driver.implicitly_wait(3)
        url = 'https://www.yogiyo.co.kr/mobile/#/'
        driver.get(url)

        time.sleep(7)
        driver.execute_script('document.getElementsByClassName("btn btn-default ico-pick")[0].click();')
        self.selenium_js(driver)
        driver.close()


start_crawling = Crawling()
start_crawling.crawl()
