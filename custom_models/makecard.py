import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction

def course_classification(line_bot_api, event):
    line_bot_api.reply_message(  # 回復傳入的訊息文字
        event.reply_token,
        TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='你想選哪個類型的課呢',
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='系所班級',
                        text='系所班級'
                    ),
                    MessageTemplateAction(
                        label='體育',
                        text='體育'
                    ),
                    MessageTemplateAction(
                        label='通識',
                        text='通識'
                    ),
                    MessageTemplateAction(
                        label='其他',
                        text='其他'
                    )
                ]
            )
        )
    )
        
def other_course_classification(line_bot_api, event):  
    line_bot_api.reply_message(  # 回復傳入的訊息文字
        event.reply_token,
        TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='其他課程分類',
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='跨領域',
                        text='跨領域'
                    ),
                    MessageTemplateAction(
                        label='就業',
                        text='就業'
                    ),
                    MessageTemplateAction(
                        label='微型',
                        text='微型'
                    ),
                    MessageTemplateAction(
                        label='PBL',
                        text='PBL'
                    )
                ]
            )
        )
    )
def general_education_classification(line_bot_api, event):  
    line_bot_api.reply_message(  # 回復傳入的訊息文字
        event.reply_token,
        TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='通識課程分類',
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='天',
                        text='天'
                    ),
                    MessageTemplateAction(
                        label='人',
                        text='人'
                    ),
                    MessageTemplateAction(
                        label='物',
                        text='物'
                    ),
                    MessageTemplateAction(
                        label='我',
                        text='我'
                    )
                ]
            )
        )
    )