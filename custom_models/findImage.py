from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage

import random
from flask import render_template
import requests
from bs4 import BeautifulSoup

line_bot_api = LineBotApi('access token')

def find_image(text):
    
    try:
        q_string = text # 設定搜尋文字
        url = "https://www.google.com/search?q=" + q_string + "&tbm=isch" # 設定抓圖片網址
        headers = {'User-Agent':'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'}

        req = requests.get(url, headers = headers)
        soup = BeautifulSoup(req.text, 'html.parser') # 爬蟲
        items = soup.find_all( "img" ) # 取出圖片網址
        random_img_url = items[random.randint(3, len(items)-1)]['data-src'] # 隨機取出圖片
        img_url = str(random_img_url)
        print( "找到圖片嚕!!!" )
        return img_url
    except:
        print( "沒找到圖片!" )
        return None