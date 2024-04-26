import json
import requests
import time
from pprint import pprint

def get_info_menu(restaurant_code,output):
    print('這裡是get_info_menu')
    url = f'https://tw.fd-api.com/api/v5/vendors/{restaurant_code}'
    query = {
        'include': 'menus',
        'language_id': '6',
        'dynamic_pricing': '0',
        'opening_type': 'delivery',
        'longitude': 121.2407764,    # 非必要(影響顯示距離)
        'latitude': 24.9573827
    }
    r = requests.get(url=url, params=query)
    if r.status_code == requests.codes.ok:
        data = r.json()
        output += str(data['data']['hero_image']) + '\n'
        output += str(data['data']['latitude']) + '+' + str(data['data']['longitude']) + '\n'
        output += str(data['data']['rating']) + '分\n'
        output += str(round(data['data']['distance'],2)) + '公里\n'
        # n = 0
        # m = 0
        # num = len(data['data']['menus'][0]['menu_categories'])
        # while m < num :
        #     num2 = len(data['data']['menus'][0]['menu_categories'][m]['products'])
        #     while n < num2 :
                # output += data['data']['menus'][0]['menu_categories'][m]['products'][n]['name'] 
                # output += data['data']['menus'][0]['menu_categories'][m]['products'][n]['description'] 
                # print(data['data']['menus'][0]['menu_categories'][m]['products'][n]['name'])
                # print(data['data']['menus'][0]['menu_categories'][m]['products'][n]['description'])
            #     n+=1
            # m += 1
            # n = 0

        # print(data['data']['minimum_delivery_fee']) #最小外送價錢
        # print(data['data']['minimum_delivery_time']) #最小外送時間
        # print(data['data']['rating']) #餐廳評分
        # print(data['data']['distance']) #距離
    else:
        print('找餐廳細項失敗')

    return output




def findMenu(restaurant_code):
    # print("這裡是findMenu")
    output = ''
    url = f'https://tw.fd-api.com/api/v5/vendors/{restaurant_code}'
    query = {
        'include': 'menus',
        'language_id': '6',
        'dynamic_pricing': '0',
        'opening_type': 'delivery',

    }
    #121.2407764 24.9573827
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    r = requests.get(url=url, params=query,headers = headers)
    if r.status_code == requests.codes.ok:
        data = r.json()
        n = 0
        m = 0
        while m < len(data['data']['menus'][0]['menu_categories'])-1:
            while n < len(data['data']['menus'][0]['menu_categories'][m]['products'])-1 :
                output += data['data']['menus'][0]['menu_categories'][m]['products'][n]['name'] + '\n'
                output += str(data['data']['menus'][0]['menu_categories'][m]['products'][n]['product_variations'][0]['price']) + '\n'
                output += data['data']['menus'][0]['menu_categories'][m]['products'][n]['description'] + '\n'

                n += 1

            m += 1
            n = 0
        output += data['data']['menus'][0]['menu_categories'][m]['products'][len(data['data']['menus'][0]['menu_categories'][m]['products'])-1]['name'] + '\n'
        output += str(data['data']['menus'][0]['menu_categories'][m]['products'][len(data['data']['menus'][0]['menu_categories'][m]['products'])-1]['product_variations'][0]['price']) + '\n'
        output += data['data']['menus'][0]['menu_categories'][m]['products'][len(data['data']['menus'][0]['menu_categories'][m]['products'])-1]['description']



    else:
        print(r.status_code)
    return output
        
def findRestaurantCode(str):
    print("進findRestaurantCode了")
    store_code = []
    url = 'https://disco.deliveryhero.io/search/api/v1/feed'
    payload = {
        'q': str,
        'location': {
            'point': {
                'longitude': 121.2407764,  # 經度
                'latitude': 24.9573827  # 緯度
            }
        },
        'config': 'Variant17',
        'vertical_types': ['restaurants'],
        'include_component_types': ['vendors'],
        'include_fields': ['feed'],
        'language_id': '6',
        'opening_type': 'delivery',
        'platform': 'web',
        'language_code': 'zh',
        'customer_type': 'regular',
        'limit': 48,  # 一次最多顯示幾筆(預設 48 筆)
        'offset': 0,  # 偏移值，想要獲取更多資料時使用
        'dynamic_pricing': 0,
        'brand': 'foodpanda',
        'country_code': 'tw',
        'use_free_delivery_label': False
    }
    headers = {
        'content-type': "application/json",
    }
    r = requests.post(url=url, data=json.dumps(payload), headers=headers)
    if r.status_code == requests.codes.ok:
        data = r.json()
        restaurants = data['feed']['items'][0]['items']
        for restaurant in restaurants[:3]:
            store_code.append(restaurant['code'])
            print(restaurant['code'])
    
    return store_code


def findRestaurant(str):
    
    url = 'https://disco.deliveryhero.io/search/api/v1/feed'
    eat =""
    payload = {
        'q': str, #食物種類
        'location': {
            'point': {
                'longitude': 121.2407764,  # 經度
                'latitude': 24.9573827  # 緯度
            }
        },
        'config': 'Variant17',
        'vertical_types': ['restaurants'],
        'include_component_types': ['vendors'],
        'include_fields': ['feed'],
        'language_id': '6',
        'opening_type': 'delivery',
        'platform': 'web',
        'language_code': 'zh',
        'customer_type': 'regular',
        'limit': 48,  # 一次最多顯示幾筆(預設 48 筆)
        'offset': 0,  # 偏移值，想要獲取更多資料時使用
        'dynamic_pricing': 0,
        'brand': 'foodpanda',
        'country_code': 'tw',
        'use_free_delivery_label': False
       
    }
    headers = {
        'content-type': "application/json",
    }
    r = requests.post(url=url, data=json.dumps(payload), headers=headers)
    if r.status_code == requests.codes.ok:
        data = r.json()
        i = 1
        print(data['feed']['count'])
        restaurants = data['feed']['items'][0]['items']
        store_code = []
        for restaurant in restaurants[:6]:
            restaurant_code = restaurant['code']
            store_code.append(restaurant['code'])
            print('這裡是findRestaurant')
            
            if i <= 3:
                eat += restaurant['name'] + '\n'
                eat = get_info_menu(restaurant_code,eat)
                i = i + 1
            
            
    else:
        print('請求失敗')

    print(store_code)
    eat += '\n可以選擇一家有興趣的!我會給老闆看看菜單喔!'
    
    return eat,store_code

def restaurant_change(restaurant_code):
    print('這裡是restaurant_change')
    output = ''
    url = f'https://tw.fd-api.com/api/v5/vendors/{restaurant_code}'
    query = {
        'include': 'menus',
        'language_id': '6',
        'dynamic_pricing': '0',
        'opening_type': 'delivery',
        'longitude': 121.2407764,    # 非必要(影響顯示距離)
        'latitude': 24.9573827
    }
    r = requests.get(url=url, params=query)
    if r.status_code == requests.codes.ok:
        data = r.json()
        output += str(data['data']['name']) + '\n'
        output += str(data['data']['hero_image']) + '\n'
        output += str(data['data']['latitude']) + '+' + str(data['data']['longitude']) + '\n'
        output += str(data['data']['rating']) + '分\n'
        output += str(round(data['data']['distance'],2)) + '公里\n'
        

    else:
        print('找餐廳細項失敗')

    return output

def is__busy(restaurant_code):
    print("這裡是findMenu")
    output = ''
    
    url = f'https://tw.fd-api.com/api/v5/vendors/{restaurant_code}'
    query = {
        'include': 'menus',
        'language_id': '6',
        'dynamic_pricing': '0',
        'opening_type': 'delivery',
        'longitude': 121.2407764,    # 非必要(影響顯示距離)
        'latitude': 24.9573827
    }
    
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    r = requests.get(url=url, params=query,headers = headers)
    if r.status_code == requests.codes.ok:
        data = r.json()
        if data['data']['is_busy'] == True :
            output = '現在很忙欸!!要不要晚點再來'
        else :
            output = '現在店家不忙喔!快去點餐吧!'

    return output

def findOpeningTime(restaurant_code):
    output = ''
    url = f'https://tw.fd-api.com/api/v5/vendors/{restaurant_code}'
    query = {
        'include': 'menus',
        'language_id': '6',
        'dynamic_pricing': '0',
        'opening_type': 'delivery',
        'longitude': 121.2407764,    # 非必要(影響顯示距離)
        'latitude': 24.9573827
    }
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    r = requests.get(url=url, params=query,headers=headers)
    if r.status_code == requests.codes.ok:
        data = r.json()
        
        i = 0
        tf = True
        weekday = ''
        
        while i < len(data['data']['schedules']) and data['data']['schedules'][i]['opening_type'] == 'delivering':
            if str(data['data']['schedules'][i]['weekday']) == '1':
                weekday = '一'
            elif str(data['data']['schedules'][i]['weekday']) == '2':
                weekday = '二'
            elif str(data['data']['schedules'][i]['weekday']) == '3':
                weekday = '三'
            elif str(data['data']['schedules'][i]['weekday']) == '4':
                weekday = '四'
            elif str(data['data']['schedules'][i]['weekday']) == '5':
                weekday = '五'
            elif str(data['data']['schedules'][i]['weekday']) == '6':
                weekday = '六'
            elif str(data['data']['schedules'][i]['weekday']) == '7':
                weekday = '日'
            if i == len(data['data']['schedules'])-1 :
                output += '星期'+ weekday + '\n'
                output += data['data']['schedules'][i]['opening_time'] + '~' + data['data']['schedules'][i]['closing_time']+ '\n'
            elif(data['data']['schedules'][i]['weekday'] != data['data']['schedules'][i+1]['weekday']):
                output += '星期'+ weekday + '\n'
                output += data['data']['schedules'][i]['opening_time'] + '~' + data['data']['schedules'][i]['closing_time']+ '\n'
                
                
            else:
                output += '星期'+ weekday+ '\n'
                output += data['data']['schedules'][i]['opening_time']+ '~' + data['data']['schedules'][i]['closing_time']+ '\n'
                
                
                output += '星期'+ weekday+ '\n'
                output += data['data']['schedules'][i+1]['opening_time']+ '~' + data['data']['schedules'][i+1]['closing_time']+ '\n'
                

                i += 2
                tf = False

            if tf :    
                i += 1 
    else:
        print('找餐廳細項失敗')

    return output


# if __name__ == '__main__':
#     pprint(findRestaurant('炸雞'))

# findRestaurant('義大利麵')
# print(findRestaurant('義大利麵'))