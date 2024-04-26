import requests
import random
import json
from bs4 import BeautifulSoup
from custom_models import make_flex_search_result, findImage

def Search( query, userid ) :
    q_string = query # 設定搜尋文字
    url = "https://www.google.com/search?q=" + q_string  # 設定要爬蟲的網址 
    headers = {'User-Agent':'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'}

    req = requests.get(url, headers = headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    #items = soup.find_all( "g-card" )
    items = soup.find_all( "a" ) # 擷取搜尋到的網址
    item = None
    link = None
    while item == None : # 隨機取出結果
        if (len(items)-19) > 30 : # 長度30以上通常為一般搜尋結果(19以下可能為google自身的地圖服務之類的)
            item = items[random.randint(30, len(items)-19)]
        elif len(items) > 30 :
            item = items[random.randint(30, len(items))]
        else : 
            item = items[random.randint(1, len(items))]
        if item != None :
            link = item.get('href')
            if link == None or ( "/search?q=" in link ) or ( ".cn" in link ) : 
                item = None
    result = []
    string = "萌萌幫您找到" + query + "的搜尋結果!"
    result.append( string )
    result.append( link )
    image = None 
    try :
        image = item.find('img')['data-src'] # 看文章裏面有沒有圖片
    except : # 沒圖片就隨機抓類似圖
        image = findImage.find_image(query)
        if image == None :
            image = "https://i.imgur.com/xjZiet7.png"
    result.append( image )
    return make_flex_search_result.set_flex_search_result(result, userid)

