from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage


import random

# 我們的函數
from custom_models import set_record, CallDatabase
# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('access token')

def insert_record(event):
        
    record_list = set_record.prepare_record(event)
    reply = CallDatabase.line_insert_record(record_list)

    return reply

def insert_location(event):
        
    record_list = set_record.prepare_location_record(event)
    reply = CallDatabase.line_insert_location(record_list)

    return True
    
def insert_time(event):
    record_list = set_record.prepare_time_record(event)
    reply = CallDatabase.line_insert_time(record_list)
    return True


    

    