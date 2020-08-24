import requests
from bs4 import BeautifulSoup


class CrawlingBS:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko)'
                      'Chrome/83.0.4103.106 Safari/537.36 '
    }
    url = 'https://www.yogiyo.co.kr/mobile/#/260195/'
    html = requests.get(url, headers=headers).text

    soup = BeautifulSoup(html, 'html.parser')
    print(soup)
    # rest_name = soup.find('div', class_='restaurant-title').text.strip().replace('\n', '')
    # print(rest_name)



start_crawling = CrawlingBS()
start_crawling
