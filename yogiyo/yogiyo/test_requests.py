import requests

s = requests.Session()

# r = s.get('https://www.yogiyo.co.kr/mobile/#/260195/', cookies={'from-my': 'browser'})
s.headers.update({
    'x-apikey': 'iphoneap',
    'x-apisecret': 'fe5183cc3dea12bd0ce299cf110a75a2'
})
r = s.get(
    'https://www.yogiyo.co.kr/api/v1/restaurants/284075/menu/?add_photo_menu=android&add_one_dish_menu=true&order_serving_type=delivery')

import ast

# print(type(r.content))
# print(r.content)

# dict_str = r.content.decode("utf-8")
# print(dict_str)
mydata = ast.literal_eval('uc2a4')
# print(repr(mydata))
# print(r.content)
