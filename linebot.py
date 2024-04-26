from __future__ import unicode_literals
from cgitb import text
from decimal import localcontext
import os
import re
from typing import Collection
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import PostbackEvent,MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate,LocationMessage
from linebot.models import MessageTemplateAction, FlexSendMessage, QuickReplyButton, MessageAction, QuickReply, URIAction,LocationAction,DatetimePickerAction
from custom_models import putRecord, convert_to_image, CourseQuery, search_data, Add_Course, GetMyMentor, Feedback, config
from custom_models import Get_bus_min_distance,bus,bike,Get_log_lat,Bubble,train
from custom_models import library_request
from custom_models import CourseRecommend, numOfComment, ClassLearned, MakeList, textComment
from custom_models import Restaurant, randomTaste,ClassLearned
import json
import dialogflow
from google.api_core.exceptions import InvalidArgument
import pymongo
from datetime import datetime
import pytz

app = Flask(__name__)


# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi(config.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.CHANNEL_SECRET)

UserNm = ""
UserPasswd = ""


def parse_user_text(text,ID): #傳訊息給dialogflow並得到解析後的答案
    #設定相關資料 
    DIALOGFLOW_PROJECT_ID = 'ai3--fsqa'
    DIALOGFLOW_LANGUAGE_CODE = 'zh-TW'#這裡很重要 mimo有兩個語系 en和zh-TW 這兩個的對話是不同的
    SESSION_ID = ID
    text_to_be_analyzed = text #要分析的句子 根據你目前設定好的即可

    #將私鑰的json檔放好，給路徑
    credential_path = "/app/other/key.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

 
    # 將要分析的句子送入dialogflow，並由dialogflow回傳對應的話->response
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    return response

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(PostbackEvent)
def handle_message(event):
    client = pymongo.MongoClient(config.MONGO_DB)
    db = client.test # 選擇database
    if event.postback.data == 'train_time':
        collection = db['功能使用狀況']
        temp = collection.find_one({ '功能名稱': '火車開始'})
        if temp != None:
            collection.update_one({ '功能名稱': '火車開始' },{'$set':{'使用次數':temp['使用次數']+1}})
        else:
            collection.insert_one({ '功能名稱': '火車開始','使用次數':1 })
        datetime = event.postback.params['datetime']
        putRecord.insert_time(event)
        msg = Bubble.Train_area('起點')
        line_bot_api.reply_message( event.reply_token, FlexSendMessage(alt_text = '選擇地區',contents =msg) )
        
    elif event.postback.data == 'favourite_route':
        client = pymongo.MongoClient(config.MONGO_DB)
        db = client.test
        collection = db['正查詢路線']
        route = collection.find_one({'UserID' : event.source.user_id})
        datetime = event.postback.params['datetime']
        origin =''
        end = ''
        route = route['路線']
        for i in route:
            if i != 't':
                origin += i
            else:
                break
        T =False
        end = ''
        for i in route:
            if i == 'o':
                T =True
            elif T:
                end += i
        result = train.train(datetime,origin,end)
         
        if result == []:
            line_bot_api.reply_message( event.reply_token, TextSendMessage(text="目前無法到達唷!") )   
        bubble =[]
        msg = []
        quick_reply_list = []
        reply_list = []
        temp =[]
        mode = 0
        if len(result) > 10:
            temp = result[:10]
            result = result[10:]
            collection = db['剩餘火車資訊']
            mode = 1
            if collection.find_one({ 'UserID' : event.source.user_id}) != None:
                collection.update_one({ 'UserID' : event.source.user_id},{'$set':{'火車資訊':result}})
            else:
                collection.insert_one({ 'UserID' : event.source.user_id,'火車資訊':result})
        else:
            mode = 2
            temp = result
            collection.delete_one({ 'UserID' : event.source.user_id})
        for i in range(len(temp)):
            bubble.append(Bubble.train_information(temp[i]))
        carousel = Bubble.make_carousel(bubble)
        msg = FlexSendMessage(alt_text='列車資訊',contents=carousel)
        reply_list.append(msg)
        collection = db['起點車站']
        origin = collection.find_one({ 'UserID' : event.source.user_id})
        origin = origin['站名']
        collection = db['終點車站']
        end = collection.find_one({ 'UserID' : event.source.user_id})
        end = end['站名']
        collection = db['火車常用路線']
        route = collection.find_one({ 'UserID' : event.source.user_id})
        if mode == 1:
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='更多火車資訊', text='@更多火車資訊')) )
            if route != None:
                route = route['常用路線']
            else:
                space = '新增火車路線'
                route_list = [space,space,space,space,space]
                collection.insert_one({ 'UserID' : event.source.user_id,'常用路線':route_list})
                route = collection.find_one({ 'UserID' : event.source.user_id})
                route = route['常用路線']
            if origin+'to'+end not in route :
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='加入火車常用路線', text='加入常用火車路線')) )
            reply_list.append( TextSendMessage( text='需要更多火車資訊嗎?', quick_reply=QuickReply(items=quick_reply_list) ) )
        else:
            if route != None:
                route = route['常用路線']
            else:
                space = '新增火車路線'
                route_list = [space,space,space,space,space]
                collection.insert_one({ 'UserID' : event.source.user_id,'常用路線':route_list})
            if origin+'to'+end not in route :
                print('不在清單內')
                quick_reply_list = []
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='加入常用火車路線', text='加入常用火車路線')) )
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='完成', text='完成')) )
                reply_list.append( TextSendMessage( text='已完成查詢，請問需要將此次查詢路線加到常用清單內嗎?', quick_reply=QuickReply(items=quick_reply_list) ) )
            else:
                reply_list.append( TextSendMessage( text='已完成查詢，此路線已存於常用清單內，如欲再次查詢，請點選常用路線即可。' ) )        
        line_bot_api.reply_message( event.reply_token,reply_list )
        
@handler.add(MessageEvent,message=LocationMessage)
def reply_text_message(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        # try:
        data = parse_user_text('起點',event.source.user_id)
        putRecord.insert_location(event)# 儲存使用者的話
        reply_dialogflow = []
        state = UseDialogflow(data, event, reply_dialogflow, '')# 去dialogflow分析意圖
        if state == 2 : # 為1就代表用了dialogflow-->跟課程相關的意圖
            reply = data.query_result.fulfillment_text
            line_bot_api.reply_message( event.reply_token, TextSendMessage(text=reply) )   
        elif state == 0 : # 非課程相關意圖
            print("用Google Search")
            line_bot_api.reply_message(event.reply_token, reply_dialogflow ) # 回復使用者

@handler.add(MessageEvent, message=TextMessage)
def reply_text_message(event):
    print(event.message.text)
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
    # if event.source.user_id != "Ucc6518f109ac9b19bc3f619594ecd2fb": # 我的
        # try : 
        data = parse_user_text(event.message.text,event.source.user_id) # 去dialogflow分析意圖
        time = putRecord.insert_record(event) # 儲存使用者的話
        reply_dialogflow = []
        state = UseDialogflow(data, event, reply_dialogflow, time) # 看是不是排課意圖
        if state == 2 : # 為1就代表用了dialogflow-->跟課程相關的意圖
            reply = data.query_result.fulfillment_text
            line_bot_api.reply_message( event.reply_token, TextSendMessage(text=reply) )   
        elif state == 0 : # 非課程相關意圖
            print("用Google Search")
            my_contents = search_data.Search(event.message.text, event.source.user_id)
            message = FlexSendMessage( alt_text='令人意外的結果', contents = my_contents ) # 做卡片式訊息
            reply_dialogflow.append( message )
            line_bot_api.reply_message(event.reply_token, reply_dialogflow ) # 回復使用者
        # except :
        #     try : 
        #         print("用Google Search_2")
        #         my_contents = search_data.Search(event.message.text, event.source.user_id)
        #         message = FlexSendMessage( alt_text='令人意外的結果', contents = my_contents ) # 做卡片式訊息
        #         reply_dialogflow.append( message )
        #         line_bot_api.reply_message(event.reply_token, reply_dialogflow ) # 回復使用者
        #     except :
        #         print('!!')
        #         line_bot_api.reply_message( event.reply_token, TextSendMessage(text="萌萌不太清楚你的意思...\n可以請你再說一次嗎?") )   

        
def UseDialogflow(data, event, reply_dialogflow, time):
    # 連接MongoDB
    print(data.query_result)
    client = pymongo.MongoClient("")
    db = client.test # 選擇database
    db2 = client.User_Message
    if event.message.type == 'text':
        if '確定覆蓋' in event.message.text : # 當衝堂時會詢問使用者是否要覆蓋-->要覆蓋課程
            collection = db['暫存即將加入課程資料'] # 衝堂的課程資訊
            course_data = collection.find_one( { 'UserID' : event.source.user_id },{ "_id" : 0 } )
            if course_data != None : # 要加入衝堂的課程資訊
                Add_Course.Add_Course_Directly( db, event.source.user_id, course_data['課程名稱'], course_data['時間'], True )
                del_query = { 'UserID' : event.source.user_id }
                collection.delete_one( del_query ) # 加好課了 清掉temp
                reply_arr = []
                # 詢問使用者是否要繼續修改課表
                quick_reply_list = []
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Add', text='@加入課程')) )
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Delete', text='@刪除課程')) )
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Done', text='@完成課表')) )
                reply_arr.append( TextSendMessage( text='請問要繼續修改課表嗎~?', quick_reply=QuickReply(items=quick_reply_list) ) )
                line_bot_api.reply_message( event.reply_token, reply_arr )
                return 1
        else : # 不要覆蓋課程 直接都清掉
            collection = db['暫存即將加入課程資料']
            del_query = { 'UserID' : event.source.user_id }
            collection.delete_one( del_query ) # 加好課了 清掉temp
            if '不要覆蓋' in event.message.text : # 清掉之前暫存的課程資訊
                reply_arr = []
                quick_reply_list = []
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Add', text='@加入課程')) )
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Delete', text='@刪除課程')) )
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Done', text='@完成課表')) )
                reply_arr.append( TextSendMessage( text='請問要繼續修改課表嗎~?', quick_reply=QuickReply(items=quick_reply_list) ) )
                line_bot_api.reply_message( event.reply_token, reply_arr )
                return 1
            elif '清空條件' in event.message.text : # 清空暫存的篩選條件
                collection_cond = db['暫存排課條件']
                del_query = { 'UserID' : event.source.user_id }
                collection_cond.delete_one( del_query ) # 加好課了 清掉temp
                reply_arr = []
                quick_reply_list = []
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Add', text='@加入課程')) )
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Delete', text='@刪除課程')) )
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Done', text='@完成課表')) )
                reply_arr.append( TextSendMessage( text="已清空條件~") )
                reply_arr.append( TextSendMessage( text='請問要繼續修改課表嗎~?', quick_reply=QuickReply(items=quick_reply_list) ) )
                line_bot_api.reply_message( event.reply_token, reply_arr )
                return 1
            elif '取消' == event.message.text : # 要取消動作
                line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="已取消動作~")
                    )  
                return 1
        if data.query_result.fulfillment_text == 'error' : # 不是預設的東西-->非排課意圖 要做google search
            print("進入未設定")
            return 0
            #reply = findImage.find_image(event)
        elif 'Find' in data.query_result.parameters and '1' in data.query_result.fulfillment_text : # 直接查詢課程資訊
            reply_arr = []
            if 'Name' in data.query_result.parameters : # 查老師
                query = "授課導師"
                for teacher in data.query_result.parameters['Name'] :
                    course = CourseQuery.course_query( db, query, teacher )
                    classData = course
                    content = Add_Course.Find_Class_Data( db, event.source.user_id, classData )
                    if content != None :
                        message = FlexSendMessage( alt_text='所查到的課程資訊如下', contents = content )
                    else : 
                        reply = "未找到您有空堂的" + teacher + "老師的課程資訊!"
                        message = TextSendMessage( text = reply )
                    reply_arr.append( message )

            if 'Course_Name' in data.query_result.parameters :
                query = "課程名稱"
                for class_data in data.query_result.parameters['Course_Name'] :
                    course = CourseQuery.course_query( db, query, class_data )
                    classData = course
                    content = Add_Course.Find_Class_Data( db, event.source.user_id, classData )
                    if content != None :
                        message = FlexSendMessage( alt_text='所查到的課程資訊如下', contents = content )
                    else : 
                        reply = "未找到您有空堂的" + teacher + "的課程資訊!"
                        message = TextSendMessage( text = reply )
                    reply_arr.append( message )
            if 'sportname' in data.query_result.parameters :
                query = "課程名稱"
                for class_data in data.query_result.parameters['sportname'] :
                    course = CourseQuery.course_query( db, query, class_data )
                    classData = course
                    content = Add_Course.Find_Class_Data( db, event.source.user_id, classData )
                    if content != None :
                        message = FlexSendMessage( alt_text='所查到的課程資訊如下', contents = content )
                    else : 
                        reply = "未找到您有空堂的" + teacher + "的課程資訊!"
                        message = TextSendMessage( text = reply )
                    reply_arr.append( message )   
            if 'Department_Name' in data.query_result.parameters :
                query = "系所班級"
                for department in data.query_result.parameters['Department_Name'] : 
                    collection = db['department_data']
                    class_data = collection.find_one({ '班級' : { '$regex': department } },{ "_id" : 0 })
                    if class_data == None :
                        course = CourseQuery.course_query( db, query, department )
                        if course == None :
                            reply = "未找到" + department + "的必修課程~"
                            reply_arr.append(  TextSendMessage(text=reply) )
                        else :
                            img_url = convert_to_image.generate_departmentCourseData( db, course )
                            reply_arr.append(  ImageSendMessage(original_content_url=img_url,preview_image_url=img_url) )
                    else :
                        reply_arr.append(  ImageSendMessage(original_content_url=class_data['url'],preview_image_url=class_data['url']) )
            if 'category' in data.query_result.parameters : # 天人物我
                query = '類別'
                for category in data.query_result.parameters['category'] :
                    course = CourseQuery.course_query( db, query, category )
                    content = Add_Course.Find_Class_Data( db, event.source.user_id, course )
                    if content != None :
                        message = FlexSendMessage( alt_text='所查到的課程資訊如下', contents = content )
                    else : 
                        reply = "未找到您有空堂的" + teacher + "的課程資訊!"
                        message = TextSendMessage( text = reply )
                    reply_arr.append( message )
                
            if len( reply_arr ) == 0 : # 都沒進去
                print( "沒進去?????????????????" )
                return 0
            line_bot_api.reply_message( event.reply_token, reply_arr )
            return 1
        elif 'course_id' in data.query_result.parameters and '加課程' == data.query_result.fulfillment_text : # 使用者回傳課程代碼-->要加入課程 
            course_id = data.query_result.parameters['course_id']
            collection = db['class_table']
            collection_course = db['classdata_1111']
            course = collection_course.find_one( { '課程代碼' : course_id },{ "_id" : 0 } )
            table = collection.find_one( { '名稱' : event.source.user_id },{ "_id" : 0 } )
            time_list = [] # 存時段的字串1-12-->[0,時段1][0,時段2]
            if course['時間1'] != 'nan' : 
                for time in course['時間1'][2:] :
                    time_str = '時段' + time
                    time_list.append( [ int( course['時間1'][0] ) - 1, time_str, course['教室1'] ] )
                if course['時間2'] != 'nan' : 
                    for time in course['時間2'][2:] :
                        time_str = '時段' + time
                        time_list.append( [ int( course['時間2'][0] ) - 1, time_str, course['教室2'] ] )
                    if course['時間3'] != 'nan' : 
                        for time in course['時間3'][2:] :
                            time_str = '時段' + time
                            time_list.append( [ int( course['時間3'][0] ) - 1, time_str, course['教室3'] ] )
            for item in time_list :
                table[item[1]][item[0]] = course['課程名稱'] + "\n" + item[2]
                collection.update_one( { "名稱": event.source.user_id },{ "$set" : { item[1] : table[item[1]] } } )
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="已加入課程~")
                ) 
            return 1
        elif 'scheduling' in data.query_result.parameters : # 排課程要傳button
            quick_reply_list = []
            i = 0
            button = data.query_result.fulfillment_messages[0].quick_replies.quick_replies
            while i < len( button ) :
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label=button[i], text=button[i])) )
                i = i + 1
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=data.query_result.fulfillment_messages[0].quick_replies.title,
                    quick_reply=QuickReply(items=quick_reply_list)
                )
            ) 
            
            return 1
        elif 'empty_course_table' in data.query_result.parameters : # 空課表要傳button 還要清空課表
            collection = db['class_table']
            del_query = { '名稱' : event.source.user_id }
            try :
                collection.delete_one( del_query )
            except :
                print( "沒有這個東西" )
            class_list = [ " ", " ", " ", " ", " ", " ", " " ]
            new_query = { '名稱' : event.source.user_id, '班級' : "", '時段A' : class_list.copy(), 
                    '時段1' : class_list.copy(), '時段2' : class_list.copy(), 
                    '時段3' : class_list.copy(), '時段4' : class_list.copy(), 
                    '時段B' : class_list.copy(), '時段5' : class_list.copy(), 
                    '時段6' : class_list.copy(), '時段7' : class_list.copy(), 
                    '時段8' : class_list.copy(), '時段C' : class_list.copy(), 
                    '時段D' : class_list.copy(), '時段E' : class_list.copy(), 
                    '時段F' : class_list.copy(), '時段G' : class_list.copy() }
            collection.insert_one( new_query ) 
            quick_reply_list = []
            i = 0
            button = data.query_result.fulfillment_messages[0].quick_replies.quick_replies
            while i < len( button ) :
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label=button[i], text=button[i])) )
                i = i + 1
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=data.query_result.fulfillment_messages[0].quick_replies.title,
                    quick_reply=QuickReply(items=quick_reply_list)
                )
            ) 
            
            return 1
        elif "current_course_table" in data.query_result.parameters : # 使用目前課表
            collection = db['class_table']
            class_data = collection.find_one( { '名稱' : event.source.user_id } )
            if class_data == None : # 根本沒課表要生出一個空的
                class_list = [ " ", " ", " ", " ", " ", " ", " " ]
                new_query = { '名稱' : event.source.user_id, '班級' : "", '時段A' : class_list.copy(), 
                        '時段1' : class_list.copy(), '時段2' : class_list.copy(), 
                        '時段3' : class_list.copy(), '時段4' : class_list.copy(), 
                        '時段B' : class_list.copy(), '時段5' : class_list.copy(), 
                        '時段6' : class_list.copy(), '時段7' : class_list.copy(), 
                        '時段8' : class_list.copy(), '時段C' : class_list.copy(), 
                        '時段D' : class_list.copy(), '時段E' : class_list.copy(), 
                        '時段F' : class_list.copy(), '時段G' : class_list.copy() }
                collection.insert_one( new_query ) 
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Add', text='@加入課程')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Delete', text='@刪除課程')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Done', text='@完成課表')) )
            reply_arr.append( TextSendMessage( text='請問選擇要如何修改課表~', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'department_name' in data.query_result.parameters and '@' in data.query_result.fulfillment_text : # 要加入課程而且是系所班級的課程
            reply_arr = []
            key = data.query_result.parameters.fields['department_name'].string_value
            img_url = Add_Course.Import_Department_Course( db, event.source.user_id, key )
            if img_url == None :
                reply_arr.append( TextSendMessage(text="未找到此系所班級的必修課程~") )
            else :
                reply_arr.append(  ImageSendMessage(original_content_url=img_url,preview_image_url=img_url) )
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Add', text='@加入課程')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Delete', text='@刪除課程')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Done', text='@完成課表')) )
            reply_arr.append( TextSendMessage( text='請問要繼續修改課表嗎~?', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
            return 1
        elif 'no' in data.query_result.parameters and '@' in data.query_result.fulfillment_text : # 不匯入系所班級
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Add', text='@加入課程')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Delete', text='@刪除課程')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Done', text='@完成課表')) )
            reply_arr.append( TextSendMessage( text='請問選擇要如何修改課表~', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
            return 1
        elif 'add_course' in data.query_result.parameters : # @加入課程問要用什麼方式
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='查詢課程資訊', text='@查詢課程')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='直接輸入資料', text='@直接輸入')) )
            reply_arr.append( TextSendMessage( text='請選擇加選方式~', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
            return 1
        elif 'time' in data.query_result.parameters and 'any' in data.query_result.parameters : # 使用者直接輸入類似 1-12 PL
            course_time = data.query_result.parameters['time']
            time_list = []
            for t in course_time :
                time_list.append( [ t[0], t[2:] ] ) # 1, 12 ( 1-12 )
            success = Add_Course.Add_Course_Directly( db, event.source.user_id, data.query_result.parameters['any'][0], time_list, False )
            if success : 
                reply_arr = []
                quick_reply_list = []
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Add', text='@加入課程')) )
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Delete', text='@刪除課程')) )
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Done', text='@完成課表')) )
                reply_arr.append( TextSendMessage( text='請問要繼續修改課表嗎~?', quick_reply=QuickReply(items=quick_reply_list) ) )
                line_bot_api.reply_message( event.reply_token, reply_arr )
            else :
                collection = db['暫存即將加入課程資料']
                query = { 'UserID' : event.source.user_id, '課程名稱' : data.query_result.parameters['any'][0], '時間' : time_list }
                collection.insert_one( query )
                reply_arr = []
                quick_reply_list = []
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Yes', text='@確定覆蓋')) )
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='No', text='@不要覆蓋')) )
                reply_arr.append( TextSendMessage( text="您所提供的時間段已有課，確定要覆蓋嗎~?", quick_reply=QuickReply(items=quick_reply_list) ) )
                line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'add_query_course' in data.query_result.parameters : # 使用者加入課程時要用查詢
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程時間', text='@課程時間')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程名稱', text='@課程名稱')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程類別', text='@課程類別')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='清空條件', text='@清空條件')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='輸入完畢', text='@條件輸入完畢')) )
            reply_arr.append( TextSendMessage( text='請選擇篩選條件~', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'course_category' in data.query_result.parameters : # 加入課程的查詢課程要查天人物我的時候
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='天', text='天')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='人', text='人')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='物', text='物')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='我', text='我')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='宗哲', text='宗哲')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='人哲', text='人哲')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='公民', text='公民')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='歷史', text='歷史')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='體育', text='體育')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='軍訓', text='軍訓')) )
            
            reply_arr.append( TextSendMessage( text=data.query_result.fulfillment_text, quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'time' in data.query_result.parameters and 'course_time' in data.query_result.output_contexts[0].parameters : # 加入課程的查詢課程的時間條件要加入資料庫
            time_list = data.query_result.parameters['time']
            course_time_list = []
            for t in time_list :
                course_time_list.append( [ t[0], t[2:] ] )
            class_name = []
            course_type_list = []
            Add_Course.Add_condition( db, event.source.user_id, course_time_list, class_name, course_type_list )
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程時間', text='@課程時間')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程名稱', text='@課程名稱')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程類別', text='@課程類別')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='清空條件', text='@清空條件')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='輸入完畢', text='@條件輸入完畢')) )
            reply_arr.append( TextSendMessage( text='請問要繼續輸入篩選條件嗎~', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'course_name' in data.query_result.parameters and '條件' in data.query_result.fulfillment_text : # 加入課程的查詢課程的課名條件要加入資料庫
            class_name = data.query_result.parameters['course_name']
            course_time_list = []
            course_type_list = []
            Add_Course.Add_condition( db, event.source.user_id, course_time_list, class_name, course_type_list )
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程時間', text='@課程時間')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程名稱', text='@課程名稱')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程類別', text='@課程類別')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='清空條件', text='@清空條件')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='輸入完畢', text='@條件輸入完畢')) )
            reply_arr.append( TextSendMessage( text='請問要繼續輸入篩選條件嗎~', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'category' in data.query_result.parameters and '原本的' in data.query_result.fulfillment_text : # 加入課程的查詢課程課程類別條件要加入資料庫
            course_type_list = data.query_result.parameters['category']
            course_time_list = []
            class_name = []
            Add_Course.Add_condition( db, event.source.user_id, course_time_list, class_name, course_type_list )
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程時間', text='@課程時間')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程名稱', text='@課程名稱')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程類別', text='@課程類別')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='清空條件', text='@清空條件')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='輸入完畢', text='@條件輸入完畢')) )
            reply_arr.append( TextSendMessage( text='請問要繼續輸入篩選條件嗎~', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'cond_ok' in data.query_result.parameters : # 加入課程的查詢課程的篩選條件輸入好了
            content = Add_Course.Find_Cond_and_Add_Course( db, event.source.user_id )
            reply_list = []
            
            if content != None : # 有找到東西
                message = TextSendMessage( text = "查詢到的結果如下" )
                reply_list.append( message )
                result = FlexSendMessage( alt_text='查詢到的結果如下:', contents = content )
                reply_list.append( result )
                quick_reply_list = []
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Add', text='@加入課程')) )
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Delete', text='@刪除課程')) )
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Done', text='@完成課表')) )
                reply_list.append( TextSendMessage( text='請問要繼續修改課表嗎~?', quick_reply=QuickReply(items=quick_reply_list) ) )
            else :
                message = TextSendMessage( text = "未查到符合條件的課程資訊" )
                reply_list.append( message )
            line_bot_api.reply_message( event.reply_token, reply_list )
        elif 'time' in data.query_result.parameters and 'delete_course' in data.query_result.output_contexts[0].parameters : # 刪除課程
            time_list = data.query_result.parameters['time']
            collection = db['class_table']
            table = collection.find_one( { '名稱' : event.source.user_id },{ "_id" : 0 }  )
            del_list = []
            for time in time_list :  # [ 1-12,2-56 ]-->1-12
                for t in time[2:] :
                    t_str = "時段" + t
                    del_list.append( [ int( time[0] ) - 1, t_str ] )
            for d in del_list :
                table[d[1]][d[0]] = " "
                collection.update_one( { "名稱": event.source.user_id },{ "$set" : { d[1] : table[d[1]] } } )
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Add', text='@加入課程')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Delete', text='@刪除課程')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='Done', text='@完成課表')) )
            reply_arr.append( TextSendMessage( text='請問要繼續修改課表嗎~?', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif '@10727145去幫我查畢業門檻我是10727224' == data.query_result.fulfillment_text : # 開查畢業門檻
            # 畢業門檻-->有學號跟密碼
            std_id = data.query_result.output_contexts[1].parameters.fields['student_id'].string_value
            std_pwd = data.query_result.output_contexts[1].parameters.fields['any'].list_value.values[0].string_value
            result = GetMyMentor.GetMyMentor( event.source.user_id, std_id, std_pwd, db )
            print("successed")
            if result == None : # 帳密有錯
                reply = "帳密輸入錯誤，萌萌無法查看，可以幫萌萌檢查一下帳密是不是打錯了嗎~?"
            else :
                reply = "-----------已完成-------------\n"
                reply = reply + "查詢畢業門檻結果:\n"
                reply = reply + "畢業所需學分數: " + str( result['畢業所需學分數']) + "\n" 
                reply = reply + "目前已修: " + str( result['畢業學分數_已得'] ) + "\n"
                reply_yet = ""
                if result['體育學分_未修'] > 0 :
                    reply_yet = reply_yet + "體育還差\"" + str( result['體育學分_未修'] ) + "\"門要修\n"
                elif result['體育學分_未修'] <= 0 :
                    reply = reply + "體育\n"
                if result['基本知能_未修'] :
                    reply_yet = reply_yet + "基本知能尚未修習之課程 : \n"
                    for item in result['基本知能_未修'] : 
                        reply_yet = reply_yet + item[2] + "\n"
                # elif result['基本知能_被當'] :
                #     reply_yet = reply_yet + "基本知能被當之課程 : \n"
                #     for item in result['基本知能_被當'] : 
                #         reply_yet = reply_yet + item[1] + "\n"
                else :
                    reply = reply + "基本知能\n"
                if result['基礎通識_未修'] :
                    reply_yet = reply_yet + "基礎通識尚未修習之課程 : \n"
                    for item in result['基礎通識_未修'] : 
                        reply_yet = reply_yet + item[2] + "\n"
                # elif result['基礎通識_被當'] :
                #     reply_yet = reply_yet + "基礎通識被當之課程 : \n"
                #     for item in result['基礎通識_被當'] : 
                #         reply_yet = reply_yet + item[1] + "\n"
                else :
                    reply = reply + "基礎通識必修\n"
                numOfcourse = ( int( result['延伸通識總學分'] ) - int( result['延伸通識學分_已得'] ) ) / 2
                numOfcourse = int( numOfcourse )
                if not result['延伸_天'] :
                    reply_yet = reply_yet + "必須要選一門延伸通識天類\n"
                    numOfcourse = numOfcourse - 1
                if not result['延伸_人'] :
                    reply_yet = reply_yet + "必須要選一門延伸通識人類\n"
                    numOfcourse = numOfcourse - 1
                if not result['延伸_物'] :
                    reply_yet = reply_yet + "必須要選一門延伸通識物類\n"
                    numOfcourse = numOfcourse - 1
                if not result['延伸_我'] :
                    reply_yet = reply_yet + "必須要選一門延伸通識我類\n"
                    numOfcourse = numOfcourse - 1
                if numOfcourse > 0 :
                    reply_yet = reply_yet + "還要從延伸通識的天人物我中任選\"" + str( numOfcourse ) + "\"門課唷\n"
                else :
                    reply = reply + "延伸通識選修\n"
                point = int( result['系選總學分'] ) - int( result['系選學分_已得'] )
                if point > 0 :
                    reply_yet = reply_yet + "系選還需要再修" + str( point ) + "學分的課\n"
                if not result['英文檢定'] :
                    reply_yet = reply_yet + "尚未通過英文畢業門檻，要記得去考唷!"
                else :
                    reply = reply + "英文門檻\n"
                reply = reply + "-----------尚未修完-------------\n" + reply_yet
                collection = db['MyMentor']
                collection.delete_one( { 'UserID' : event.source.user_id } )
                collection.insert_one( result )
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=reply)
                )  
            return 1
        elif 'complete_course_table' in data.query_result.parameters : # 完成課表-->生成課表圖片
            collection = db['class_table']
            class_data = collection.find_one({ '名稱' : event.source.user_id },{ "_id" : 0 })
            if class_data == None :
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="您好像還沒做課表唷~\n要不要做一下課表~\n(可以按選單左上角的按鈕做課表唷!)")
                ) 
            else : 
                img_url = convert_to_image.Generate_new_table( db, class_data )
                reply_arr = []
                reply_arr.append(  ImageSendMessage(original_content_url=img_url,preview_image_url=img_url) )
                line_bot_api.reply_message( event.reply_token, reply_arr )
            
            return 1
        elif 'direct_input' in data.query_result.parameters : # @直接輸入-->要請使用者說條件才能加入課程
            return 2
        elif 'feedback' in data.query_result.parameters : # 使用者要告狀萌萌的問題
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=URIAction(label='填表單', uri='https://forms.gle/eJHP7kGxeNGXWh3E6')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='直接跟萌萌說', text='直接跟萌萌說')) )
            reply_arr.append( TextSendMessage( text=data.query_result.fulfillment_text, quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif "@reply1" == data.query_result.fulfillment_text : # 使用者說了第一句萌萌的壞話
            collection = db['意見回饋']
            query = { 'UserID' : event.source.user_id, '問題' : data.query_result.query_text }
            collection.insert_one(query)
            line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "這樣啊~ 萌萌知道了! \n那還有什麼想對萌萌說的嗎~" ) )
        elif "@reply2" == data.query_result.fulfillment_text : # 使用者說了第2句萌萌的壞話或者沒事了 要傳訊息給我們的信箱
            collection = db['意見回饋']
            problem = collection.find_one({ 'UserID' : event.source.user_id },{ "_id" : 0 })
            reply = '使用者 : ' + event.source.user_id + "\n問題 : \n" + problem['問題'] + "\n" + data.query_result.query_text + "\n"
            collection.delete_one( { 'UserID' : event.source.user_id } )
            Feedback.Feedback(reply)
            line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "恩恩! 謝謝你讓萌萌知道你的想法\n好~謝謝你告訴萌萌" ) )

#-------------------------------------------------------------------課程----------------------------------------------------
        elif '取得修課資料' == data.query_result.fulfillment_text : 
            cam_collection = db2[event.source.user_id]
            temp = cam_collection.find_one({'Msg':event.message.text,'Date': time})
            cam_collection.update_one({'Msg':event.message.text,'Date':time},{'$set':{'功能':'取得修課資料'}})

            std_id = data.query_result.output_contexts[0].parameters.fields['student_id'].string_value
            std_pwd = data.query_result.output_contexts[0].parameters.fields['any'].list_value.values[0].string_value
            collection = db['存已修課程']
            class_list = ClassLearned.GetMySelf( std_id, std_pwd )
            temp1 = []
            temp2 = []
            temp3 = []
            temp4 = []
            temp5 = []
            temp6 = []
            for s in class_list :
                temp1.append(s[0])
                temp2.append(s[1])
                temp3.append(s[2])
                temp4.append(s[3])
                temp5.append(s[4])
                temp6.append('N')
            query_insert = { 'UserID' : event.source.user_id, '學號' : std_id, '課程年分' : temp1, '課程代碼' : temp2, '課程名稱' : temp3, '學分' : temp4, '分數' : temp5, '評價狀態' : temp6 }
            collection.insert_one( query_insert )
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='評價課程', text='@評價課程')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='查詢修課清單',text='@查詢修課清單')) )
            reply_arr.append( TextSendMessage( text='登入成功!請幫萌萌按下面的「課程評價」按鈕以繼續評分哦~\n若想查詢修課清單，請點選「查詢修課清單」按鈕。', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'findlearnedlist' in data.query_result.parameters :
            cam_collection = db2[event.source.user_id]
            temp = cam_collection.find_one({'Msg':event.message.text,'Date': time})
            cam_collection.update_one({'Msg':event.message.text,'Date':time},{'$set':{'功能':'請求修課列表'}})
            img_url = MakeList.MakeList( db, event.source.user_id )
            reply_arr = []
            text = "您的修課清單如下:"
            reply_arr.append( TextSendMessage(text) )
            reply_arr.append(  ImageSendMessage(original_content_url=img_url,preview_image_url=img_url) )
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='評價課程', text='@評價課程')) )
            reply_arr.append( TextSendMessage( text='未來想查詢修課清單可以直接輸入:查詢修課清單\n想幫萌萌評價課程可以點選下方「評價課程」按鈕哦~', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'Evaluate_course' in data.query_result.parameters and '1' in data.query_result.fulfillment_text :
            cam_collection = db2[event.source.user_id]
            temp = cam_collection.find_one({'Msg':event.message.text,'Date': time})
            cam_collection.update_one({'Msg':event.message.text,'Date':time},{'$set':{'功能':'進入評價課程'}})
            collection = db['功能使用狀況']
            temp = collection.find_one({ '功能名稱': '課程評價開始'})
            if temp != None:
                collection.update_one({ '功能名稱': '課程評價開始' },{'$set':{'使用次數':temp['使用次數']+1}})
            else:
                collection.insert_one({ '功能名稱': '課程評價開始','使用次數':1 })
            collection = db['存已修課程']
            temp = collection.find_one({ 'UserID' : event.source.user_id })
            if temp == None :
                line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "請先登入，才能進行評分哦~\n在此輸入您的學號以進行登入" ) )
            else :
                collection = db['暫存評價資訊']
                del_query = { 'UserID' : event.source.user_id }
                collection.delete_one( del_query ) # 清掉temp
                reply_arr = []
                quick_reply_list = []
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='查詢修課清單', text='@查詢修課清單')) )
                reply_arr.append( TextSendMessage( text='請問要評分的課程名稱是?\n請輸入完整的課程名稱，若不清楚可參考「您的修課清單」', quick_reply=QuickReply(items=quick_reply_list) ) )
                line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'course_name' in data.query_result.parameters and '請問老師名字是' in data.query_result.fulfillment_text :
            cam_collection = db2[event.source.user_id]
            temp = cam_collection.find_one({'Msg':event.message.text,'Date': time})
            cam_collection.update_one({'Msg':event.message.text,'Date':time},{'$set':{'功能':'評價課程-輸入課程名稱'}})
            eclass_name = data.query_result.parameters['course_name']
            collection = db['暫存評價資訊']
            teacherName = ''
            className = ''
            for name in eclass_name : 
                className = name
            query = { 'UserID' : event.source.user_id, '課程名稱' : className, '老師名稱' : teacherName }
            collection.insert_one( query )
            return 2
        elif 'name' in data.query_result.parameters and '失敗' == data.query_result.fulfillment_text :
            cam_collection = db2[event.source.user_id]
            temp = cam_collection.find_one({'Msg':event.message.text,'Date': time})
            cam_collection.update_one({'Msg':event.message.text,'Date':time},{'$set':{'功能':'評價課程-輸入老師名稱'}})

            teacherName = data.query_result.parameters['name']
            for s in teacherName :
                teacherName = s
            collection = db['暫存評價資訊']
            temp = collection.find_one({ 'UserID' : event.source.user_id },{ "_id" : 0 })
            fcollection = db['存已修課程']
            class_info = fcollection.find_one({ 'UserID' : event.source.user_id })
            reply_arr = []
            quick_reply_list = []
            # 這裡是偷改的哦哦哦哦哦哦哦哦哦哦哦哦哦
            # ctcollection = db['classdata_1111']
            # theclass = ctcollection.find_one({ '課程名稱' : temp['課程名稱'] })
            # class_code = theclass['課程代碼']
            # tf = True
            # 這裡是偷改的哦哦哦哦哦哦哦哦哦哦哦哦哦
            tf = False
            if class_info != None :
                i = 0
                for s in class_info['課程名稱'] :
                    if s == temp['課程名稱'] :
                        class_year = class_info['課程年分'][i]
                        class_code = class_info['課程代碼'][i]
                        year = 'classdata_' + class_year
                        ctcollection = db[year]
                        hasClass = ctcollection.find_one({ '課程名稱' : s ,'課程代碼' : class_code })
                        if hasClass != None :
                            class_type = hasClass['類別']
                            if hasClass['授課導師'] == teacherName :
                                tf = True
                                comStatus = class_info['評價狀態'][i]
                                break
                    i = i + 1
            temp['老師名稱'] = teacherName
            collection.update_one({ 'UserID' : event.source.user_id },{ "$set": { '課程名稱' : temp['課程名稱'], '老師名稱' : temp['老師名稱'], '課程代碼' : class_code, '課程類別' : class_type } })
            temp = collection.find_one({ 'UserID' : event.source.user_id })
            if tf :
                if comStatus == 'N' :
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='作業量', text='作業量')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程難易度', text='課程難易度')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='學到東西多寡', text='學到東西多寡')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='給分甜不甜', text='給分甜不甜')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='不了', text='不了')) )
                    reply_arr.append( TextSendMessage( text='要評價下列哪一個項目呢?\n(已經評論過的項目將不再顯示，無法更改，請謹慎評分!)', quick_reply=QuickReply(items=quick_reply_list) ) )
                elif comStatus == 'T' :
                    temp_com_collection = db['暫存課程評價']
                    tempComment = temp_com_collection.find_one({ 'UserID' : event.source.user_id, '課程名稱' : temp['課程名稱'], '老師名稱' : teacherName, '課程代碼' : class_code,'課程類別' : class_type })
                    if tempComment['作業量分數'] == '0' :
                        quick_reply_list.append( QuickReplyButton(action=MessageAction(label='作業量', text='作業量')) )
                    if tempComment['課程難度分數'] == '0' :
                        quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程難易度', text='課程難易度')) )
                    if tempComment['學到東西分數'] == '0' :
                        quick_reply_list.append( QuickReplyButton(action=MessageAction(label='學到東西多寡', text='學到東西多寡')) )
                    if tempComment['給分甜不甜分數'] == '0' :
                        quick_reply_list.append( QuickReplyButton(action=MessageAction(label='給分甜不甜', text='給分甜不甜')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='不了', text='不了')) )
                    reply_arr.append( TextSendMessage( text='要評價下列哪一個項目呢?\n(已經評論過的項目將不再顯示，無法更改，請謹慎評分!)', quick_reply=QuickReply(items=quick_reply_list) ) )
                else :
                    com_collection = db['課程評價']
                    comment = com_collection.find_one({ '課程名稱' : temp['課程名稱'], '老師名稱' : temp['老師名稱'], '課程代碼' : temp['課程代碼'],'課程類別' : class_type })
                    for i in range( len( comment['UserID'] ) ) :
                        if comment['UserID'][i] == event.source.user_id :
                            if comment['文字評論'][i] == '' :
                                reply_arr.append( TextSendMessage( text='偵測到您還沒留過文字評價，幫忙留個言吧~' ) )
                            else :
                                reply_arr.append( TextSendMessage( text='您已經為這堂課評過分且有留文字評價囉，可以幫忙評價其他課程!' ) )
                                del_query = ({ 'UserID' : event.source.user_id })
                                del_collection = db['暫存評價資訊']
                                del_collection.delete_one( del_query )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='再次評價', text='我想評價課程')) )
                line_bot_api.reply_message( event.reply_token, reply_arr )
            else :
                del_query = { 'UserID' : event.source.user_id }
                collection.delete_one( del_query ) # 清掉temp
                line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "您好像沒修過這堂課，或輸入有誤哦~\n請檢查後重新輸入，感謝您。" ) )
        elif 'score' in data.query_result.parameters :
            # 偷偷弄抽獎↓
            # fcollection = db['存已修課程']
            # temp = fcollection.find_one({ "UserID" : event.source.user_id })
            # std_id = temp['學號']
            # collection = db['抽獎名單']
            # temp1 = collection.find_one({ "學號" : std_id })
            # if temp1 == None :
            #     collection.insert_one({ "學號" : std_id })
            # 偷偷弄抽獎↑
            score = data.query_result.parameters['score']
            for s in score :
                score = s
            collection = db['存已修課程']
            tempInfo_collection = db['暫存評價資訊']
            temp_collection = db['暫存課程評價']
            hisList = collection.find_one( { 'UserID' : event.source.user_id } )
            tempInfo = tempInfo_collection.find_one({ 'UserID' : event.source.user_id })

            cam_collection = db2[event.source.user_id]
            temp = cam_collection.find_one({'Msg':event.message.text,'Date':time})
            cam_collection.update_one({'Msg':event.message.text,'Date':time},{'$set':{'功能':'評價課程-輸入'+tempInfo['Subject']}})
            
            for i in range( len(hisList['課程名稱']) ) :
                if tempInfo['課程名稱'] == hisList['課程名稱'][i] and tempInfo['課程代碼'] == hisList['課程代碼'][i] :
                    status = hisList['評價狀態'][i]
            print(status)
            class_type = tempInfo['課程類別']
            shw = ""
            shard = ""
            slearn = ""
            ssweet = ""
            reply_arr = []
            quick_reply_list = []
            if tempInfo['Subject'] == "作業量分數" :
                shw = score
            elif tempInfo['Subject'] == "課程難度分數" :
                shard = score
            elif tempInfo['Subject'] == "學到東西分數" :
                slearn = score
            elif tempInfo['Subject'] == "給分甜不甜分數" :
                ssweet = score
            if status == 'N' :
                if len( shw ) == 0 :
                    shw = '0'
                if len( shard ) == 0 :
                    shard = '0'
                if len( slearn ) == 0 :
                    slearn = '0'
                if len( ssweet ) == 0 :
                    ssweet = '0'
                comment = ""
                query = { 'UserID' : event.source.user_id, '課程名稱' : tempInfo['課程名稱'], '老師名稱' : tempInfo['老師名稱'], 
                        '課程代碼' : tempInfo['課程代碼'],'課程類別' : class_type, '作業量分數' : shw, '課程難度分數' : shard, '學到東西分數' : slearn,
                        '給分甜不甜分數' : ssweet, '文字評論' : comment }
                temp_collection.insert_one( query )
                for i in range( len( hisList['評價狀態'] ) ) :
                    if hisList['課程名稱'][i] == tempInfo['課程名稱'] and hisList['課程代碼'][i] == tempInfo['課程代碼'] :
                        hisList['評價狀態'][i] = 'T'
                        status = 'T'
                        collection.update_one( { 'UserID' : event.source.user_id }, { "$set" : { '評價狀態' : hisList['評價狀態'] } } )
            elif status == 'T' :
                temp_collection.update_one( { 'UserID' : event.source.user_id, '課程名稱' : tempInfo['課程名稱'], '課程代碼' : tempInfo['課程代碼'],'課程類別' : class_type }
                                            ,{ "$set" : { tempInfo['Subject'] : score } }  )
                hisTemp = temp_collection.find_one( { 'UserID' : event.source.user_id, '課程名稱' : tempInfo['課程名稱'], '課程代碼' : tempInfo['課程代碼'],'課程類別' : class_type } )
                if hisTemp['作業量分數'] != '0' and hisTemp['課程難度分數'] != '0' and hisTemp['學到東西分數'] != '0' and hisTemp['給分甜不甜分數'] != '0' :
                    for i in range( len( hisList['評價狀態'] ) ) :
                        if hisList['課程名稱'][i] == tempInfo['課程名稱'] and hisList['課程代碼'][i] == tempInfo['課程代碼'] :
                            hisList['評價狀態'][i] = 'Y'
                            status = 'Y'
                            collection.update_one( { 'UserID' : event.source.user_id }, { "$set" : { '評價狀態' : hisList['評價狀態'] } } )
                    com_collection = db['課程評價']
                    comInfo = com_collection.find_one({ '課程名稱' : hisTemp['課程名稱'], '老師名稱' : hisTemp['老師名稱'],'課程類別' : class_type })
                    if comInfo == None :
                        s1 = []
                        s2 = []
                        s3 = []
                        s4 = []
                        s5 = []
                        s6 = []
                        s1.append( event.source.user_id )
                        s2.append( hisTemp['作業量分數'] )
                        s3.append( hisTemp['課程難度分數'] )
                        s4.append( hisTemp['學到東西分數'] )
                        s5.append( hisTemp['給分甜不甜分數'] )
                        s6.append( hisTemp['文字評論'] )
                        query = { '課程名稱' : hisTemp['課程名稱'], '老師名稱' : hisTemp['老師名稱'], '課程代碼' : hisTemp['課程代碼'],'課程類別' : class_type, 'UserID' : s1,
                                '作業量分數' : s2, '課程難度分數' : s3, '學到東西分數' : s4, '給分甜不甜分數' : s5, '文字評論' : s6 }
                        com_collection.insert_one( query )
                    else :
                        comInfo['UserID'].append( hisTemp['UserID'] )
                        comInfo['作業量分數'].append( hisTemp['作業量分數'] )
                        comInfo['課程難度分數'].append( hisTemp['課程難度分數'] )
                        comInfo['學到東西分數'].append( hisTemp['學到東西分數'] )
                        comInfo['給分甜不甜分數'].append( hisTemp['給分甜不甜分數'] )
                        comInfo['文字評論'].append( hisTemp['文字評論'] )
                        com_collection.update_one( { '課程名稱' : hisTemp['課程名稱'], '老師名稱' : hisTemp['老師名稱'],'課程類別' : class_type }
                                                    ,{ "$set" : { 'UserID' : comInfo['UserID'], '作業量分數' : comInfo['作業量分數'], '課程難度分數' : comInfo['課程難度分數'],
                                                    '學到東西分數' : comInfo['學到東西分數'], '給分甜不甜分數' : comInfo['給分甜不甜分數'], '文字評論' : comInfo['文字評論'] } } )
            if status != 'Y' :
                hisTemp = temp_collection.find_one( { 'UserID' : event.source.user_id, '課程名稱' : tempInfo['課程名稱'], '課程代碼' : tempInfo['課程代碼'],'課程類別' : class_type } )
                if hisTemp['作業量分數'] == '0' :
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='作業量', text='作業量')) )
                if hisTemp['課程難度分數'] == '0' :
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程難易度', text='課程難易度')) )
                if hisTemp['學到東西分數'] == '0' :
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='學到東西多寡', text='學到東西多寡')) )
                if hisTemp['給分甜不甜分數'] == '0' :
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='給分甜不甜', text='給分甜不甜')) )
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='不了', text='不了')) )
                reply_arr.append( TextSendMessage( text='還要評價下列哪一個項目呢?', quick_reply=QuickReply(items=quick_reply_list) ) )
            else :
                collection = db['功能使用狀況']
                temp = collection.find_one({ '功能名稱': '課程評價結束'})
                if temp != None:
                    collection.update_one({ '功能名稱': '課程評價結束' },{'$set':{'使用次數':temp['使用次數']+1}})
                else:
                    collection.insert_one({ '功能名稱': '課程評價結束','使用次數':1 })
                class_name = hisTemp['課程名稱']
                teacherName = hisTemp['老師名稱']
                class_code = hisTemp['課程代碼']
                del_query = { 'UserID' : event.source.user_id, '課程名稱' : hisTemp['課程名稱'], '課程代碼' : hisTemp['課程代碼'], '老師名稱' : hisTemp['老師名稱'], '課程類別' : class_type }
                temp_collection.delete_one( del_query )
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='再次評價', text='我想評價課程')) )
                scoreList = numOfComment.Count( db, class_name, teacherName, class_code )############################
                reply_arr.append( TextSendMessage( text='感謝您評價，看看其他人怎麼評:' ) )
                if scoreList != None :
                    str_List = []
                    if scoreList[0] < 20 : str_List.append( "超多的" )
                    elif scoreList[0] >= 20 and scoreList[0] < 40 : str_List.append( "算偏多" )
                    elif scoreList[0] >= 40 and scoreList[0] < 60 : str_List.append( "一般般" )
                    elif scoreList[0] >= 60 and scoreList[0] < 80 : str_List.append( "還算少" )
                    elif scoreList[0] >= 80 : str_List.append( "超少的" )
                    if scoreList[1] < 20 : str_List.append( "超級難" )
                    elif scoreList[1] >= 20 and scoreList[1] < 40 : str_List.append( "有點難" )
                    elif scoreList[1] >= 40 and scoreList[1] < 60 : str_List.append( "一般般" )
                    elif scoreList[1] >= 60 and scoreList[1] < 80 : str_List.append( "蠻簡單" )
                    elif scoreList[1] >= 80 : str_List.append( "超簡單" )
                    if scoreList[2] < 20 : str_List.append( "學不到" )
                    elif scoreList[2] >= 20 and scoreList[2] < 40 : str_List.append( "學一點" )
                    elif scoreList[2] >= 40 and scoreList[2] < 60 : str_List.append( "一般般" )
                    elif scoreList[2] >= 60 and scoreList[2] < 80 : str_List.append( "學不少" )
                    elif scoreList[2] >= 80 : str_List.append( "學很多" )
                    if scoreList[3] < 20 : str_List.append( "有夠苦" )
                    elif scoreList[3] >= 20 and scoreList[3] < 40 : str_List.append( "有點苦" )
                    elif scoreList[3] >= 40 and scoreList[3] < 60 : str_List.append( "一般般" )
                    elif scoreList[3] >= 60 and scoreList[3] < 80 : str_List.append( "還算甜" )
                    elif scoreList[3] >= 80 : str_List.append( "超級甜" )
                    outPutCard = Bubble.endCommentResult( scoreList, class_name, str_List )
                    result = FlexSendMessage( alt_text='看看其他人怎麼評:', contents = outPutCard )
                    reply_arr.append( result )
                else :
                    reply_arr.append( TextSendMessage( text='尚未蒐集到其他人的評價。' ) )######################
                if hisTemp['文字評論'] == "" :
                    text='偵測到您還未對' + hisTemp['課程名稱'] + '留過評論，留點評論吧！(直接輸入文字即可評論，文字評論後續無法進行修改，請謹慎評論！)\n或是按下面按鈕再評一堂~'
                else :
                    text='偵測到您已留過文字評價，感謝您使用我們的評價系統，點擊下方按鈕再評一堂吧!'
                reply_arr.append( TextSendMessage( text, quick_reply=QuickReply(items=quick_reply_list)  ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'Find' in data.query_result.parameters and 'Evaluate_course' in data.query_result.parameters :
            del_query = { 'UserID' : event.source.user_id }
            collection = db['排序']
            collection.delete_many( del_query )
            collection = db['暫存推薦條件']
            collection.delete_many( del_query )
            collection = db['下一批']
            collection.delete_many( del_query )
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='系上的課', text='系上的課')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='通識課', text='通識課')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='用課名查詢', text='指定課名')) )
            reply_arr.append( TextSendMessage( text='請問想看哪種課程的推薦呢', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'department_recommend' in data.query_result.parameters :
            line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "請輸入系所名字(如:資訊、應外)\n若有組別請加上(如:工業工程組、化工綠能組)" ) )
        elif 'generaleducation' in data.query_result.parameters :
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='天', text='天')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='人', text='人')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='物', text='物')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='我', text='我')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='宗哲', text='宗哲')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='人哲', text='人哲')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='公民', text='公民')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='歷史', text='歷史')) )
            reply_arr.append( TextSendMessage( text='請輸入課程類別(例如: 天 、人哲.. )\n因為課程很多，所以一次只能輸入一個類別唷', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'specific_course' in data.query_result.parameters :
            line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "請輸入課程名稱" ) )
        elif 'course_name' in data.query_result.parameters and '查特定評價' in data.query_result.fulfillment_text :
            s_name = data.query_result.parameters['course_name']
            for s in s_name :
                s_name = s
            collection = db['暫存推薦條件']
            query = { 'UserID' : event.source.user_id, '課程名稱' : s_name }
            collection.insert_one( query )
            collectionCor = db['課程評價']
            temp = collectionCor.find({ '課程名稱' : s_name })
            if temp != None :
                u = []
                for s in temp :
                    tf = True
                    if len(u) == 0 :
                        u.append(s['老師名稱'])
                    else :
                        for i in range(len(u)) :
                            if u[i] == s['老師名稱'] :
                                tf = False
                        if tf :
                            u.append(s['老師名稱'])
                cardList = []
                for s in u :
                    cardList.append( Bubble.teacherButton(s) )
                toSent = Bubble.chooseTeacher( cardList )
                reply_arr = []
                result = FlexSendMessage( alt_text='選擇教授', contents = toSent )
                reply_arr.append( result )
                line_bot_api.reply_message( event.reply_token, reply_arr )
            else :
                reply_arr.append( TextSendMessage( text='目前沒有相應的評價內容哦，請再次嘗試~' ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'Name' in data.query_result.parameters and '查評價用' in data.query_result.fulfillment_text :
            t_name = data.query_result.parameters['Name']
            for s in t_name :
                t_name = s
            collection = db['暫存推薦條件']
            collection.update_one({ 'UserID' : event.source.user_id },{ "$set" : { '老師名稱' : t_name } })
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='作業量', text='作業量')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程難易度', text='課程難易度')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='學到東西多寡', text='學到東西多寡')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='給分甜不甜', text='給分甜不甜')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='沒有', text='沒有')) )
            reply_arr.append( TextSendMessage( text='有特別看重哪項嗎', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'category' in data.query_result.parameters and 'min_distance' not in data.query_result.parameters :
            c_name = data.query_result.parameters['category']
            for s in c_name :
                c_name = s
            collection = db['暫存推薦條件']
            query = { 'UserID' : event.source.user_id, '類別' : c_name }
            collection.insert_one( query )
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='作業量', text='作業量')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程難易度', text='課程難易度')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='學到東西多寡', text='學到東西多寡')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='給分甜不甜', text='給分甜不甜')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='沒有', text='沒有')) )
            reply_arr.append( TextSendMessage( text='有特別看重哪項嗎', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'Only_Department' in data.query_result.parameters :
            d_name = data.query_result.parameters['Only_Department']
            for s in d_name :
                d_name = s
            collection = db['暫存推薦條件']
            query = { 'UserID' : event.source.user_id, '系級' : d_name }
            collection.insert_one( query )
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='作業量', text='作業量')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='課程難易度', text='課程難易度')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='學到東西多寡', text='學到東西多寡')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='給分甜不甜', text='給分甜不甜')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='沒有', text='沒有')) )
            reply_arr.append( TextSendMessage( text='有特別看重哪項嗎', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif ( 'subject' in data.query_result.parameters or 'no' in data.query_result.parameters ) and '特定課程' in data.query_result.fulfillment_text :
            cam_collection = db2[event.source.user_id]
            temp = cam_collection.find_one({'Msg':event.message.text,'Date':time})
            cam_collection.update_one({'Msg':event.message.text,'Date':time},{'$set':{'功能':'課程推薦-特定課程'}})

            temp = data.query_result.parameters['subject']
            if len( temp ) == 0 :
                temp = "No"
            else :
                for s in temp :
                    temp = s
            courseList = []
            courseList.append( CourseRecommend.Recommend_SpecificCourse( event.source.user_id, temp, db ) )
            if courseList != None :
                reply_arr = []
                quick_reply_list = []
                carouselList = []
                for s in courseList :
                    s['加權分數'] = str(s['加權分數'])
                    carouselList.append( Bubble.cardCourse( s['課程名稱'], s['課程代碼'], s['老師名稱'], s['加權分數'] ) )
                outputCard = Bubble.carousel( carouselList )
                result = FlexSendMessage( alt_text='推薦結果:', contents = outputCard )
                reply_arr.append( result )
                line_bot_api.reply_message( event.reply_token, reply_arr )
            else :
                line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "查無評價，請重新嘗試~" ) )
        elif ( 'subject' in data.query_result.parameters or 'no' in data.query_result.parameters ) and '類別' in data.query_result.fulfillment_text :
            cam_collection = db2[event.source.user_id]
            temp = cam_collection.find_one({'Msg':event.message.text,'Date':time})
            cam_collection.update_one({'Msg':event.message.text,'Date':time},{'$set':{'功能':'課程推薦-通識課'}})

            temp = data.query_result.parameters['subject']
            for s in temp :
                temp = s
            if len(temp) == 0 :
                temp = "No"
            courseList = CourseRecommend.Recommend_GeneralEducation( event.source.user_id, temp, db )
            if courseList != None :
                carouselList = []
                for s in courseList :
                    s['加權分數'] = str(s['加權分數'])
                    carouselList.append( Bubble.cardCourse( s['課程名稱'], s['課程代碼'], s['老師名稱'], s['加權分數'] ) )
                outputCard = Bubble.carousel( carouselList )
                result = FlexSendMessage( alt_text='推薦結果:', contents = outputCard )
                reply_arr = []
                quick_reply_list = []
                reply_arr.append( result )
                collection = db['下一批']
                temp = collection.find_one({ "UserID" : event.source.user_id })
                if temp != None :
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='看下一組', text='看下一組')) )
                    reply_arr.append( TextSendMessage( text='可點選下方按鈕看下一組哦~', quick_reply=QuickReply(items=quick_reply_list) ) )
                line_bot_api.reply_message( event.reply_token, reply_arr )
            else :
                line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "查無評價，請重新嘗試~" ) )
        elif ( 'subject' in data.query_result.parameters or 'no' in data.query_result.parameters ) and '系級' in data.query_result.fulfillment_text :
            cam_collection = db2[event.source.user_id]
            temp = cam_collection.find_one({'Msg':event.message.text,'Date':time})
            cam_collection.update_one({'Msg':event.message.text,'Date':time},{'$set':{'功能':'課程推薦-系選修'}})

            temp = data.query_result.parameters['subject']
            for s in temp :
                temp = s
            if len(temp) == 0 :
                temp = "No"
            courseList = CourseRecommend.Recommend_DepartmentCourse( event.source.user_id, temp, db )
            if courseList != None :
                carouselList = []
                for s in courseList :
                    s['加權分數'] = str(s['加權分數'])
                    carouselList.append( Bubble.cardCourse( s['課程名稱'], s['課程代碼'], s['老師名稱'], s['加權分數'] ) )
                outputCard = Bubble.carousel( carouselList )
                result = FlexSendMessage( alt_text='推薦結果:', contents = outputCard )
                reply_arr = []
                quick_reply_list = []
                reply_arr.append( result )
                collection = db['下一批']
                temp = collection.find_one({ "UserID" : event.source.user_id })
                if temp != None :
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='看下一組', text='看下一組')) )
                    reply_arr.append( TextSendMessage( text='可點選下方按鈕看下一組哦~', quick_reply=QuickReply(items=quick_reply_list) ) )
                line_bot_api.reply_message( event.reply_token, reply_arr )
            else :
                line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "查無評價，請重新嘗試~" ) )
        elif 'nextsetofcourse' in data.query_result.parameters :
            reply_arr = []
            quick_reply_list = []
            collection = db['下一批']
            temp = collection.find_one({ 'UserID' : event.source.user_id })
            cardList = []
            if ( temp['case'] == 1 ) :
                courseList = CourseRecommend.makeTop10List( event.source.user_id, db, 2 )
                for s in courseList :
                    s['加權分數'] = str(s['加權分數'])
                    cardList.append( Bubble.cardCourse( s['課程名稱'], s['課程代碼'], s['老師名稱'], s['加權分數'] ) )
            elif ( temp['case'] == 2 ) :
                courseList = textComment.returnUnused( db, event.source.user_id )
                for s in courseList :
                    cardList.append( Bubble.textCommentCard( s['課程名稱'], s['課程代碼'], s['老師名稱'], s['文字評論'] ) )
            outputCard = Bubble.carousel( cardList )
            result = FlexSendMessage( alt_text='結果如下:', contents = outputCard )
            reply_arr.append( result )
            collection = db['下一批']
            temp = collection.find_one({ "UserID" : event.source.user_id })
            if temp != None :
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='看下一組', text='看下一組')) )
                reply_arr.append( TextSendMessage( text='可點選下方按鈕看下一組哦~', quick_reply=QuickReply(items=quick_reply_list) ) )
            else :
                reply_arr.append( TextSendMessage( text='到底了唷' ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'course_id' in data.query_result.parameters and 'course_name' in data.query_result.parameters :
            cam_collection = db2[event.source.user_id]
            temp = cam_collection.find_one({'Msg':event.message.text,'Date':time})
            cam_collection.update_one({'Msg':event.message.text,'Date':time},{'$set':{'功能':'課程推薦-看文字評論'}})

            courseName = data.query_result.parameters.fields['course_name'].list_value.values[0].string_value
            courseId = data.query_result.parameters.fields['course_id'].list_value.values[0].string_value
            tempList = textComment.outputTextComment( db, event.source.user_id, courseName, courseId )
            reply_arr = []
            quick_reply_list = []
            tf = False
            if tempList != None :
                toConvertList = []
                if len( tempList ) <= 10 :
                    for s in tempList :
                        toConvertList.append( Bubble.textCommentCard( courseName, s['課程代碼'], s['老師名稱'], s['文字評論'] ) )
                    tf = True
                elif len( tempList ) > 10 :
                    for i in range( 10 ) :
                        toConvertList.append( Bubble.textCommentCard( courseName, tempList[i]['課程代碼'], tempList[i]['老師名稱'], tempList[i]['文字評論'] ) )
                toSent = Bubble.carousel( toConvertList )
                result = FlexSendMessage( alt_text='結果如下:', contents = toSent )
                reply_arr.append( result )
            else :
                reply_arr.append( TextSendMessage( text='沒有找到有關的文字評論哦~' ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'no' in data.query_result.parameters :
            cam_collection = db2[event.source.user_id]
            temp = cam_collection.find_one({'Msg':event.message.text,'Date':time})
            cam_collection.update_one({'Msg':event.message.text,'Date':time},{'$set':{'功能':'中離課程評論'}})

            collection = db['功能使用狀況']
            temp = collection.find_one({ '功能名稱': '課程評價不了'})
            if temp != None:
                collection.update_one({ '功能名稱': '課程評價不了' },{'$set':{'使用次數':temp['使用次數']+1}})
            else:
                collection.insert_one({ '功能名稱': '課程評價不了','使用次數':1 })
            collection = db['暫存評價資訊']
            temp = collection.find_one({ "UserID" : event.source.user_id })
            class_name = temp['課程名稱']
            class_code = temp['課程代碼']
            class_type = temp['課程類別']
            teacherName = temp['老師名稱']
            collection = db['課程評價']
            temp1 = collection.find_one({'課程名稱' : class_name, '課程代碼' : class_code, '老師名稱' : teacherName,'課程類別' : class_type})
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='再次評價', text='我想評價課程')) )
            scoreList = numOfComment.Count( db, class_name, teacherName, class_code )############################
            reply_arr.append( TextSendMessage( text='感謝您評價，看看其他人怎麼評:' ) )
            if scoreList != None :
                str_List = []
                if scoreList[0] < 20 : str_List.append( "超多的" )
                elif scoreList[0] >= 20 and scoreList[0] < 40 : str_List.append( "算偏多" )
                elif scoreList[0] >= 40 and scoreList[0] < 60 : str_List.append( "一般般" )
                elif scoreList[0] >= 60 and scoreList[0] < 80 : str_List.append( "還算少" )
                elif scoreList[0] >= 80 : str_List.append( "超少的" )
                if scoreList[1] < 20 : str_List.append( "超級難" )
                elif scoreList[1] >= 20 and scoreList[1] < 40 : str_List.append( "有點難" )
                elif scoreList[1] >= 40 and scoreList[1] < 60 : str_List.append( "一般般" )
                elif scoreList[1] >= 60 and scoreList[1] < 80 : str_List.append( "蠻簡單" )
                elif scoreList[1] >= 80 : str_List.append( "超簡單" )
                if scoreList[2] < 20 : str_List.append( "學不到" )
                elif scoreList[2] >= 20 and scoreList[2] < 40 : str_List.append( "學一點" )
                elif scoreList[2] >= 40 and scoreList[2] < 60 : str_List.append( "一般般" )
                elif scoreList[2] >= 60 and scoreList[2] < 80 : str_List.append( "學不少" )
                elif scoreList[2] >= 80 : str_List.append( "學很多" )
                if scoreList[3] < 20 : str_List.append( "有夠苦" )
                elif scoreList[3] >= 20 and scoreList[3] < 40 : str_List.append( "有點苦" )
                elif scoreList[3] >= 40 and scoreList[3] < 60 : str_List.append( "一般般" )
                elif scoreList[3] >= 60 and scoreList[3] < 80 : str_List.append( "還算甜" )
                elif scoreList[3] >= 80 : str_List.append( "超級甜" )
                outPutCard = Bubble.endCommentResult( scoreList, class_name, str_List )
                result = FlexSendMessage( alt_text='看看其他人怎麼評:', contents = outPutCard )
                reply_arr.append( result )
            else :
                reply_arr.append( TextSendMessage( text='尚未蒐集到其他人的評價。' ) )######################
            his_list_collection = db['存已修課程']
            hisList = his_list_collection.find_one( { 'UserID' : event.source.user_id } )
            for i in range( len( hisList['評價狀態'] ) ) :
                if hisList['課程名稱'][i] == class_name and hisList['課程代碼'][i] == class_code :
                    status = hisList['評價狀態'][i]
            if status == 'T' :
                temp_com_collection = db['暫存課程評價']
                tempComment = temp_com_collection.find_one({ 'UserID' : event.source.user_id, '課程名稱' : class_name,'老師名稱' : teacherName, '課程代碼' : class_code })
                if tempComment != None :
                    if len( tempComment['文字評論'] ) == 0 :
                        text = "偵測到您還未對" + class_name + "留過評論，留點評論吧！(直接輸入文字即可評論，文字評論後續無法進行修改，請謹慎評論！)\n或是按下面按鈕再評一堂~"
                    else :
                        text = "感謝您熱心評價，您可能會想..."
                        quick_reply_list.append( QuickReplyButton(action=MessageAction(label='給我們反饋', text='feedback')) )
            elif status == 'N' :
                text = "偵測到您還未對" + class_name + "留過評論，留點評論吧！(直接輸入文字即可評論，文字評論後續無法進行修改，請謹慎評論！)\n或是按下面按鈕再評一堂~"
            reply_arr.append( TextSendMessage( text, quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif '文字評論' in data.query_result.fulfillment_text :
            cam_collection = db2[event.source.user_id]
            temp = cam_collection.find_one({'Msg':event.message.text,'Date':time})
            cam_collection.update_one({'Msg':event.message.text,'Date':time},{'$set':{'功能':'課程推薦-輸入文字評論'}})

            comment = data.query_result.query_text
            collection = db['暫存評價資訊']
            temp = collection.find_one({ 'UserID' : event.source.user_id })
            if temp != None :
                class_name = temp['課程名稱']
                class_code = temp['課程代碼']
                class_type = temp['課程類別']
                teacherName = temp['老師名稱']
                status_collection = db['存已修課程']
                hisList = status_collection.find_one({ 'UserID' : event.source.user_id })
                reply_arr = []
                for i in range( len( hisList['評價狀態'] ) ) :
                    if hisList['課程名稱'][i] == class_name and hisList['課程代碼'][i] == class_code :
                        status = hisList['評價狀態'][i]
                if status == 'Y' :
                    collection = db['課程評價']
                    temp = collection.find_one({ '課程名稱' : class_name, '老師名稱' : teacherName, '課程代碼' : class_code,'課程類別' : class_type })
                    for i in range( len( temp['文字評論'] ) ) :
                        if temp['UserID'][i] == event.source.user_id :
                            if len( temp['文字評論'][i] ) != 0 :
                                reply_arr.append( TextMessage( text = "您已留過文字評論囉~" ) )
                            else :
                                temp['文字評論'][i] = comment
                                collection.update_one( { '課程名稱' : class_name, '老師名稱' : teacherName, '課程代碼' : class_code },
                                                        { "$set" : { '文字評論' : temp['文字評論'] } } )
                else :
                    collection = db['暫存課程評價']
                    hisTemp = collection.find_one( { 'UserID' : event.source.user_id, '課程名稱' : class_name, '課程代碼' : class_code, '老師名稱' : teacherName,'課程類別' : class_type } )
                    if hisTemp != None :
                        hisTemp['文字評論'] = comment
                        collection.update_one( { 'UserID' : event.source.user_id, '課程名稱' : hisTemp['課程名稱'], '課程代碼' : hisTemp['課程代碼'], '老師名稱' : hisTemp['老師名稱'],'課程類別' : class_type },
                                                { "$set" : { '文字評論' : hisTemp['文字評論'] } } )
                    else :
                        query = { 'UserID' : event.source.user_id, '課程名稱' : class_name, '老師名稱' : teacherName, '課程代碼' : class_code,'課程類別' : class_type,
                                '作業量分數' : "0", '課程難度分數' : "0", '學到東西分數' : "0", '給分甜不甜分數' : "0", '文字評論' : comment }
                        collection.insert_one( query )
                        for i in range( len( hisList['評價狀態'] ) ) :
                            if hisList['課程名稱'][i] == class_name and hisList['課程代碼'][i] == class_code :
                                hisList['評價狀態'][i] = "T"
                                status_collection.update_one( { 'UserID' : event.source.user_id },{ "$set" : { '評價狀態' : hisList['評價狀態'] } } )
                collection = db['暫存評價資訊']
                collection.delete_one({ 'UserID' : event.source.user_id })
                quick_reply_list = []
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='再評一堂吧', text='我想評價課程')) )
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='給我們反饋~', text='feedback')) )
                reply_arr.append( TextSendMessage( text='感謝您留文字評論！\n您可能會想...', quick_reply=QuickReply(items=quick_reply_list) ) )
                line_bot_api.reply_message( event.reply_token, reply_arr )
            else :
                return 0
        elif 'subject' in data.query_result.parameters and '2' in data.query_result.fulfillment_text :
            cam_collection = db2[event.source.user_id]
            temp = cam_collection.find_one({'Msg':event.message.text,'Date':time})
            cam_collection.update_one({'Msg':event.message.text,'Date':time},{'$set':{'功能':'課程推薦-選擇看重項目'}})

            del_query = { 'UserID' : event.source.user_id }
            collection = db['暫存分數']
            collection.delete_one( del_query )
            temp = data.query_result.parameters['subject']
            for s in temp :
                temp = s
            collection = db['暫存評價資訊']
            a = collection.find_one({ 'UserID' : event.source.user_id })
            if a != None :
                collection.update_one({ 'UserID' : event.source.user_id },{ "$set": { 'Subject' : temp } })
                reply_arr = []
                quick_reply_list = []
                if temp == '作業量分數' :
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='超多的', text='超多的')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='算偏多吧', text='算偏多吧')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='一般般', text='一般般')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='還算少', text='還算少')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='超少的', text='超少的')) )
                    reply_arr.append( TextSendMessage( text='你覺得這堂課的作業量如何呢?', quick_reply=QuickReply(items=quick_reply_list) ) )
                elif temp == '給分甜不甜分數' :
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='超苦', text='超苦')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='有點苦', text='有點苦')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='一般般', text='一般般')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='還算甜', text='還算甜')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='超甜', text='超甜')) )
                    reply_arr.append( TextSendMessage( text='你覺得這堂課老師給分甜嗎?', quick_reply=QuickReply(items=quick_reply_list) ) )
                elif temp == '課程難度分數' :
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='好難', text='好難')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='偏難', text='偏難')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='一般般', text='一般般')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='蠻簡單', text='蠻簡單')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='超簡單', text='超簡單')) )
                    reply_arr.append( TextSendMessage( text='你覺得這堂課會很難嗎?', quick_reply=QuickReply(items=quick_reply_list) ) )
                elif temp == '學到東西分數' :
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='學不太到東西', text='學不太到東西')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='只學到一點', text='只學到一點')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='一般般', text='一般般')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='能學不少', text='能學不少')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='能學很多', text='能學很多')) )
                    reply_arr.append( TextSendMessage( text='你覺得這堂課能學到很多東西嗎?', quick_reply=QuickReply(items=quick_reply_list) ) )
                line_bot_api.reply_message( event.reply_token, reply_arr )  
            else :
                line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "好像出錯了，麻煩幫我重新輸入哦~" ) )
        elif 'send_list' in data.query_result.parameters :
            line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "表單在這邊，感謝您的熱心使用~\nhttps://docs.google.com/forms/d/e/1FAIpQLScelCzgbQNx7S8e3P_n3rAyyiPuuh8gNCZjxHtClw4rpiixLw/viewform?usp=sf_link" ) )
# --------------------------------------------------交通和書籍功能-----------------------------------------------
        elif "end_inquiry" in data.query_result.parameters :
            collection = db['起點車站']
            origin = collection.find_one({ 'UserID' : event.source.user_id})
            origin = origin['站名']
            collection = db['終點車站']
            end = collection.find_one({ 'UserID' : event.source.user_id})
            end = end['站名']
            collection = db['火車常用路線']
            route = collection.find_one({ 'UserID' : event.source.user_id})
            if route != None:
                route = route['常用路線']
            else:
                space = '新增火車路線'
                route_list = [space,space,space,space,space]
                collection.insert_one({ 'UserID' : event.source.user_id,'常用路線':route_list})
            if origin+'to'+end not in route :
                reply_arr = []
                quick_reply_list = []
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='加入常用火車路線', text='加入常用火車路線')) )
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='完成', text='完成')) )
                reply_arr.append( TextSendMessage( text='請問需要將此次查詢路線加到常用清單內嗎?', quick_reply=QuickReply(items=quick_reply_list) ) )
                line_bot_api.reply_message( event.reply_token, reply_arr )
            else:
                line_bot_api.reply_message( event.reply_token, TextSendMessage(text='已結束查詢~如需再次查詢，請點選主選單之功能。') )
        
        elif"@reply_after_train_1" == data.query_result.fulfillment_text :
            collection = db['起點車站']
            origin = collection.find_one({ 'UserID' : event.source.user_id})
            origin = origin['站名']
            collection = db['終點車站']
            end = collection.find_one({ 'UserID' : event.source.user_id})
            end = end['站名']
            collection = db['火車常用路線']
            route = collection.find_one({ 'UserID' : event.source.user_id})
            if route != None:
                route = route['常用路線']
                route_list = route
            else:
                space = '新增火車路線'
                route_list = [space,space,space,space,space]
                collection.insert_one({ 'UserID' : event.source.user_id,'常用路線':route_list})
            if "新增火車路線" not in route_list:
                line_bot_api.reply_message( event.reply_token, TextSendMessage(text='常用路線清單已滿，如需更改請重設清單。') )
            else:
                for i in range(len(route_list)):
                    if route_list[i] == "新增火車路線":
                        route_list[i] = origin+'to'+end
                        break
                collection.delete_one({ 'UserID' : event.source.user_id})
                collection.insert_one({ 'UserID' : event.source.user_id,'常用路線':route_list})
                line_bot_api.reply_message( event.reply_token, TextSendMessage(text='已加入常用路線') )
        
        elif 'bike' in data.query_result.parameters :
            Bike = bike.bike()
            bubble = []
            msg = ''
            for i in range(len(Bike.Return)):
                bubble.append(Bubble.Bubble_bike(Bike.Return[i],Bike.Rent[i],Bike.Name[i],Bike.google_map[i]))
            msg = FlexSendMessage( alt_text= 'YouBike已查詢完畢!', contents = Bubble.make_carousel(bubble) )
            line_bot_api.reply_message( event.reply_token, msg  )
            return 1

        elif 'bus_Nearest' in data.query_result.parameters :
            collection = db['功能使用狀況']
            temp = collection.find_one({ '功能名稱': '最近公車開始'})
            if temp != None:
                collection.update_one({ '功能名稱': '最近公車開始' },{'$set':{'使用次數':temp['使用次數']+1}})
            else:
                collection.insert_one({ '功能名稱': '最近公車開始','使用次數':1 })
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=LocationAction(label='請輸入當前位置')) )
            reply_arr.append( TextSendMessage( text='請輸入當前位置', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
            return 1

        elif 'bus' in data.query_result.parameters :
            collection = db['功能使用狀況']
            temp = collection.find_one({ '功能名稱': '公車開始'})
            if temp != None:
                collection.update_one({ '功能名稱': '公車開始' },{'$set':{'使用次數':temp['使用次數']+1}})
            else:
                collection.insert_one({ '功能名稱': '公車開始','使用次數':1 })
            line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "請輸入欲查詢公車路線" ) )
            return 1
        elif "@reply_bus_1" == data.query_result.fulfillment_text:
            collection = db['功能使用狀況']
            temp = collection.find_one({ '功能名稱': '公車結束'})
            if temp != None:
                collection.update_one({ '功能名稱': '公車結束' },{'$set':{'使用次數':temp['使用次數']+1}})
            else:
                collection.insert_one({ '功能名稱': '公車結束','使用次數':1 })
            bus0,bus1 = bus.Get_bus(data.query_result.query_text)
            msg = ''
            bubble = []
            body0 = []
            body1 = []
            btn = []
            for i in range(len(bus0.num)):
                body0.append(Bubble.make_bus_body_tittle(str(bus0.name[i])))
                body0.append(Bubble.make_bus_body(bus0.time[i]))
            if len(bus0.num) != 0:
                bubble.append(Bubble.Bubble_bus('路線:'+str(data.query_result.query_text),'往'+bus0.name[len(bus0.name)-1],body0,btn,'#B87070'))
            for i in range(len(bus1.num)):
                body1.append(Bubble.make_bus_body_tittle(str(bus1.name[i])))
                body1.append(Bubble.make_bus_body(bus1.time[i]))
            if len(bus1.num) != 0:
                bubble.append(Bubble.Bubble_bus('路線:'+str(data.query_result.query_text),'往'+bus1.name[len(bus1.name)-1],body1,btn,'#B87070'))
            msg = FlexSendMessage( alt_text= '公車已查詢完畢!', contents = Bubble.make_carousel(bubble) )
            line_bot_api.reply_message( event.reply_token, msg )
            return 1

        elif 'min_distance' in data.query_result.parameters :
            collection = db['功能使用狀況']
            temp = collection.find_one({ '功能名稱': '行程開始'})
            if temp != None:
                collection.update_one({ '功能名稱': '行程開始' },{'$set':{'使用次數':temp['使用次數']+1}})
            else:
                collection.insert_one({ '功能名稱': '行程開始','使用次數':1 })
            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=LocationAction(label='輸入起點')) )
            reply_arr.append( TextSendMessage( text='請輸入起點', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
            return 1

        elif 'train' in data.query_result.parameters :
            reply_arr = []
            quick_reply_list = []
            today = datetime.now(pytz.timezone('Asia/Taipei')).strftime('-%m-%dt%H:%M')
            quick_reply_list.append( QuickReplyButton(action=DatetimePickerAction(label='輸入欲搜尋時間',data='train_time',mode='datetime',initial='2023'+today,  max= "2024"+today,min ='2023'+today )) )
            reply_arr.append( TextSendMessage( text='請選擇欲搜尋時間', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
            return 1
        elif "train_area" in data.query_result.parameters and"@reply_train_3" != data.query_result.fulfillment_text and "@reply_train_favourite_1" != data.query_result.fulfillment_text:
            msg = Bubble.Train_location("起點",event.message.text)
            line_bot_api.reply_message( event.reply_token, FlexSendMessage(alt_text='請選擇車站',contents=msg) )
            return 1
        elif "@reply_train_2" == data.query_result.fulfillment_text:
            collection = db['起點車站']
            if collection.find_one({ 'UserID' : event.source.user_id}) != None:
                collection.update_one({ 'UserID' : event.source.user_id},{'$set':{'站名':event.message.text}})
            else:
                collection.insert_one({ 'UserID' : event.source.user_id,'站名':event.message.text})
            msg = Bubble.Train_area("終點")
            line_bot_api.reply_message( event.reply_token, FlexSendMessage(alt_text = '選擇地區',contents =msg) )
        elif "@reply_train_3" == data.query_result.fulfillment_text:
            msg = Bubble.Train_location("終點",event.message.text)
            line_bot_api.reply_message( event.reply_token, FlexSendMessage(alt_text='請選擇車站',contents=msg) )
            return 1
        elif "@reply_train_4" == data.query_result.fulfillment_text:
            collection = db['功能使用狀況']
            temp = collection.find_one({ '功能名稱': '火車結束'})
            if collection.find_one({ 'UserID' : event.source.user_id}) != None:
                collection.update_one({ '功能名稱': '火車結束' },{'$set':{'使用次數':temp['使用次數']+1}})
            else:
                collection.insert_one({ '功能名稱': '火車結束','使用次數':1 })
            end = event.message.text
            collection = db['終點車站']
            if collection.find_one({ 'UserID' : event.source.user_id}) != None:
                collection.update_one({ 'UserID' : event.source.user_id},{'$set':{'站名':event.message.text}})
            else:
                collection.insert_one({ 'UserID' : event.source.user_id,'站名':event.message.text})
            collection = db['起點車站']
            origin = collection.find_one({ 'UserID' : event.source.user_id})
            collection = db['時間']
            time = collection.find_one({ 'UserID' : event.source.user_id})
            result = train.train(time['時間'],origin['站名'],end)
            if result == []:
                line_bot_api.reply_message( event.reply_token, TextSendMessage(text="目前無法到達唷!") )  
            bubble =[]
            msg = []
            quick_reply_list = []
            reply_list = []
            temp =[]
            mode = 0
            if len(result) > 10:
                temp = result[:10]
                result = result[10:]
                collection = db['剩餘火車資訊']
                mode = 1
                if collection.find_one({ 'UserID' : event.source.user_id}) != None:
                    collection.update_one({ 'UserID' : event.source.user_id},{'$set':{'火車資訊':result}})
                else:
                    collection.insert_one({ 'UserID' : event.source.user_id,'火車資訊':result})
            else:
                mode = 2
                temp = result
                collection.delete_one({ 'UserID' : event.source.user_id})
            for i in range(len(temp)):
                bubble.append(Bubble.train_information(temp[i]))
            carousel = Bubble.make_carousel(bubble)
            msg = FlexSendMessage(alt_text='列車資訊',contents=carousel)
            reply_list.append(msg)
            collection = db['起點車站']
            origin = collection.find_one({ 'UserID' : event.source.user_id})
            origin = origin['站名']
            collection = db['終點車站']
            end = collection.find_one({ 'UserID' : event.source.user_id})
            end = end['站名']
            collection = db['火車常用路線']
            route = collection.find_one({ 'UserID' : event.source.user_id})
            if mode == 1:
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='更多火車資訊', text='@更多火車資訊')) )
                if route != None:
                    route = route['常用路線']
                else:
                    space = '新增火車路線'
                    route_list = [space,space,space,space,space]
                    collection.insert_one({ 'UserID' : event.source.user_id,'常用路線':route_list})
                    route = collection.find_one({ 'UserID' : event.source.user_id})
                    route = route['常用路線']
                if origin+'to'+end not in route :
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='加入火車常用路線', text='加入常用火車路線')) )
                reply_list.append( TextSendMessage( text='需要更多火車資訊嗎?', quick_reply=QuickReply(items=quick_reply_list) ) )
            else:
                if route != None:
                    route = route['常用路線']
                else:
                    space = '新增火車路線'
                    route_list = [space,space,space,space,space]
                    collection.insert_one({ 'UserID' : event.source.user_id,'常用路線':route_list})
                    route = collection.find_one({ 'UserID' : event.source.user_id})
                    route = route['常用路線']
                if origin+'to'+end not in route :
                    quick_reply_list = []
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='加入常用火車路線', text='加入常用火車路線')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='完成', text='完成')) )
                    reply_list.append( TextSendMessage( text='已完成查詢，請問需要將此次查詢路線加到常用清單內嗎?', quick_reply=QuickReply(items=quick_reply_list) ) )
                else:
                    reply_list.append( TextSendMessage( text='已完成查詢，此路線已存於常用清單內，如欲再次查詢，請點選常用路線即可。' ) )
            line_bot_api.reply_message( event.reply_token,reply_list )
        elif 'more_train' in data.query_result.parameters and "@reply_train_favourite_1" != data.query_result.fulfillment_text:
            collection = db['剩餘火車資訊']
            result = collection.find_one({ 'UserID' : event.source.user_id})
            result = result['火車資訊']
            mode = 0
            bubble =[]
            msg = []
            quick_reply_list = []
            reply_list = []
            temp =[]
            if len(result) > 10:
                temp = result[:10]
                result = result[10:]
                collection = db['剩餘火車資訊']
                mode = 1
                if collection.find_one({ 'UserID' : event.source.user_id}) != None:
                    collection.update_one({ 'UserID' : event.source.user_id},{'$set':{'火車資訊':result}})
                else:
                    collection.insert_one({ 'UserID' : event.source.user_id,'火車資訊':result})
            else:
                temp = result
                collection.delete_one({ 'UserID' : event.source.user_id})
                mode = 2 
                
                
            for i in range(len(temp)):
                bubble.append(Bubble.train_information(temp[i]))
            carousel = Bubble.make_carousel(bubble)

            msg = FlexSendMessage(alt_text='列車資訊',contents=carousel)
            reply_list.append(msg)


            collection = db['起點車站']
            origin = collection.find_one({ 'UserID' : event.source.user_id})
            origin = origin['站名']
            collection = db['終點車站']
            end = collection.find_one({ 'UserID' : event.source.user_id})
            end = end['站名']
            collection = db['火車常用路線']
            route = collection.find_one({ 'UserID' : event.source.user_id})
            if mode == 1:
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='更多火車資訊', text='@更多火車資訊')) )
                if route != None:
                    route = route['常用路線']
                else:
                    space = '新增火車路線'
                    route_list = [space,space,space,space,space]
                    collection.insert_one({ 'UserID' : event.source.user_id,'常用路線':route_list})
                    route = collection.find_one({ 'UserID' : event.source.user_id})
                    route = route['常用路線']
                if origin+'to'+end not in route :
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='加入火車常用路線', text='加入常用火車路線')) )
                reply_list.append( TextSendMessage( text='需要更多火車資訊嗎?', quick_reply=QuickReply(items=quick_reply_list) ) )
            else:
                if route != None:
                    route = route['常用路線']
                else:
                    space = '新增火車路線'
                    route_list = [space,space,space,space,space]
                    collection.insert_one({ 'UserID' : event.source.user_id,'常用路線':route_list})
                if origin+'to'+end not in route :
                    quick_reply_list = []
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='加入常用火車路線', text='加入常用火車路線')) )
                    quick_reply_list.append( QuickReplyButton(action=MessageAction(label='完成', text='完成')) )
                    reply_list.append( TextSendMessage( text='已完成查詢，請問需要將此次查詢路線加到常用清單內嗎?', quick_reply=QuickReply(items=quick_reply_list) ) )
                
                else:
                    reply_list.append( TextSendMessage( text='已完成查詢，此路線已存於常用清單內，如欲再次查詢，請點選常用路線即可。') )
            line_bot_api.reply_message( event.reply_token,reply_list )

        elif "reset_train_favourite" in data.query_result.parameters:
            collection = db['火車常用路線']
            collection.delete_one({ 'UserID' : event.source.user_id})
            space = '新增火車路線'
            route_list = [space,space,space,space,space]
            collection.insert_one({ 'UserID' : event.source.user_id,'常用路線':route_list})
            line_bot_api.reply_message( event.reply_token,TextSendMessage(text = '重設完成') )


        elif "@reply_train_favourite_1" == data.query_result.fulfillment_text:
            collection = db['火車常用路線']
            route = collection.find_one({ 'UserID' : event.source.user_id})
            if route == None:
                space = '新增火車路線'
                route_list = [space,space,space,space,space]
                collection.insert_one({ 'UserID' : event.source.user_id,'常用路線':route_list})
                space = '新增火車路線'
                bubble = Bubble.train_route(space,space,space,space,space)
            else:
                route = route['常用路線']
                bubble = Bubble.train_route(route[0],route[1],route[2],route[3],route[4])
            
            line_bot_api.reply_message( event.reply_token,FlexSendMessage(alt_text='火車常用路線',contents= bubble))
            
        elif "@reply_train_favourite_2" == data.query_result.fulfillment_text:
            reply_arr = []
            quick_reply_list = []
            collection = db['正查詢路線']
            collection.delete_one({ 'UserID' : event.source.user_id})
            route = collection.insert_one({ 'UserID' : event.source.user_id,'路線':event.message.text})
            origin =''
            end = ''
            route = event.message.text
            for i in route:
                if i != 't':
                    origin += i
                else:
                    break
            T =False
            end = ''
            for i in route:
                if i == 'o':
                    T =True
                elif T:
                    end += i

            collection = db['起點車站']
            if collection.find_one({ 'UserID' : event.source.user_id}) != None:
                collection.update_one({ 'UserID' : event.source.user_id},{'$set':{ '站名': origin}})
            else:
                collection.insert_one({ 'UserID' : event.source.user_id, '站名': origin})
            collection = db['終點車站']
            if collection.find_one({ 'UserID' : event.source.user_id}) != None:
                collection.update_one({ 'UserID' : event.source.user_id},{'$set':{ '站名': end}})
            else:
                collection.insert_one({ 'UserID' : event.source.user_id, '站名': end})
                
            today = datetime.now(pytz.timezone('Asia/Taipei')).strftime('-%m-%dt%H:%M')
            quick_reply_list.append( QuickReplyButton(action=DatetimePickerAction(label='輸入欲搜尋時間',data='favourite_route',mode='datetime',initial='2023'+today,  max= "2024"+today,min ='2023'+today )) )
            reply_arr.append( TextSendMessage( text='請選擇欲搜尋時間', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
            return 1

        elif "@reply_new_train_favourite_1" == data.query_result.fulfillment_text:
            msg = Bubble.Train_area("起點")
            line_bot_api.reply_message( event.reply_token, FlexSendMessage(alt_text = '選擇地區',contents =msg) )
        elif "@reply_new_train_favourite_2" in data.query_result.parameters and"@reply_train_3" != data.query_result.fulfillment_text and "@reply_train_favourite_1" != data.query_result.fulfillment_text:
            msg = Bubble.Train_location("起點",event.message.text)
            line_bot_api.reply_message( event.reply_token, FlexSendMessage(alt_text='請選擇車站',contents=msg) )
            return 1
        elif "@reply_new_train_favourite_3" == data.query_result.fulfillment_text:
            collection = db['起點車站']
            if collection.find_one({ 'UserID' : event.source.user_id}) != None:
                collection.update_one({ 'UserID' : event.source.user_id},{'$set':{'站名':event.message.text}})
            else:
                collection.insert_one({ 'UserID' : event.source.user_id,'站名':event.message.text})
            msg = Bubble.Train_area("終點")
            line_bot_api.reply_message( event.reply_token, FlexSendMessage(alt_text = '選擇地區',contents =msg) )
        elif "@reply_new_train_favourite_4" == data.query_result.fulfillment_text:
            msg = Bubble.Train_location("終點",event.message.text)
            line_bot_api.reply_message( event.reply_token, FlexSendMessage(alt_text='請選擇車站',contents=msg) )
            return 1
        elif "@reply_new_train_favourite_5" == data.query_result.fulfillment_text:
            end = event.message.text
            collection = db['終點車站']
            try:
                collection.insert_one({ 'UserID' : event.source.user_id},{'$set':{'站名':event.message.text}})
            except:
                collection.insert_one({ 'UserID' : event.source.user_id,'站名':event.message.text})
            collection = db['起點車站']
            origin = collection.find_one({ 'UserID' : event.source.user_id})
            collection = db['火車常用路線']
            space = '新增火車路線'
            route = collection.find_one({ 'UserID' : event.source.user_id})
            if route == None:
                space = '新增火車路線'
                route_list = [space,space,space,space,space]
                collection.insert_one({ 'UserID' : event.source.user_id,'常用路線':route_list})
                route_list = [origin['站名']+'to'+end,space,space,space,space]
                collection.insert_one({ 'UserID' : event.source.user_id,'常用路線':route_list})
            else :
                route_list = route['常用路線']
                for i in range(len(route_list)):
                    if route_list[i] == space:
                        route_list[i] = origin['站名']+'to'+end
                        break
                collection.delete_one({ 'UserID' : event.source.user_id})
                collection.insert_one({ 'UserID' : event.source.user_id,'常用路線':route_list})

            line_bot_api.reply_message( event.reply_token, TextSendMessage(text='已加入常用路線') )

        elif 'book_name' in data.query_result.parameters:
            line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "請輸入欲查詢書名!" ) )

        elif "@reply_book_name" == data.query_result.fulfillment_text :
            res = []
            res = library_request.request_find(event.message.text) 
            body = []
            btn = []
            msg = ''
            bubble = []
            if res == []:
                line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "查無此書" ) )
            if len(res) > 10:
                res = res[:10]
            for i in range(len(res)):
                body = []
                for j in range(len(res[i])-1):
                    for k in range(len(res[i][j+1])):
                        body.append(Bubble.make_bus_body_tittle('館藏地'+res[i][j+1][k][0]))
                        body.append(Bubble.make_bus_body(res[i][j+1][k][1]))
                bubble.append(Bubble.Bubble_bus(res[i][0],'架上情況',body,btn,'#9999CC'))
            msg = FlexSendMessage( alt_text= '書籍已查詢完畢!', contents = Bubble.make_carousel(bubble) )
            line_bot_api.reply_message( event.reply_token, msg )

        elif "@reply_teacher_book" == data.query_result.fulfillment_text :
            book = library_request.Classnum(event.message.text,'教科書')
            if len(book) >= 1:
                print(book)
                book_name_list=[]
                for b in book[1:]:
                    book_name_list.append(Bubble.book_name_list(b))
                bubble = Bubble.book_list(book[0],book_name_list)
                line_bot_api.reply_message( event.reply_token,FlexSendMessage(alt_text='請選擇書籍',contents= bubble))
            elif len(book) == 0:
                line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "此課程無公告教科書" ) )
            else:
                line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "無此課程" ) )

        elif "@reply_teacher_book_1" == data.query_result.fulfillment_text :
            res = []
            res = library_request.request_find(event.message.text) 
            body = []
            btn = []
            msg = ''
            bubble = []
            if res == []:
                line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "查無此書" ) )
            if len(res) > 10:
                res = res[:10]
            for i in range(len(res)):
                body = []
                for j in range(len(res[i])-1):
                    for k in range(len(res[i][j+1])):
                        body.append(Bubble.make_bus_body_tittle('館藏地'+res[i][j+1][k][0]))
                        body.append(Bubble.make_bus_body(res[i][j+1][k][1]))
                bubble.append(Bubble.Bubble_bus(res[i][0],'架上情況',body,btn,'#9999CC'))
            msg = FlexSendMessage( alt_text= '書籍已查詢完畢!', contents = Bubble.make_carousel(bubble) )
            line_bot_api.reply_message( event.reply_token, msg )
        elif "@reply_course_book" == data.query_result.fulfillment_text :
            book = library_request.Classnum(event.message.text,'參考書')
            if len(book) >= 1:
                print(book)
                book_name_list=[]
                for b in book[1:]:
                    book_name_list.append(Bubble.book_name_list(b))
                bubble = Bubble.book_list(book[0],book_name_list)
                line_bot_api.reply_message( event.reply_token,FlexSendMessage(alt_text='請選擇書籍',contents= bubble))
            elif len(book) == 0:
                line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "此課程無公告參考書" ) )
            else:
                line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "無此課程" ) )

        elif "@reply_course_book_1" == data.query_result.fulfillment_text :
            res = []
            res = library_request.request_find(event.message.text) 
            body = []
            btn = []
            msg = ''
            bubble = []
            if res == []:
                line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "查無此書" ) )
            if len(res) > 10:
                res = res[:10]
            for i in range(len(res)):
                body = []
                for j in range(len(res[i])-1):
                    for k in range(len(res[i][j+1])):
                        body.append(Bubble.make_bus_body_tittle('館藏地'+res[i][j+1][k][0]))
                        body.append(Bubble.make_bus_body(res[i][j+1][k][1]))
                bubble.append(Bubble.Bubble_bus(res[i][0],'架上情況',body,btn,'#9999CC'))
            msg = FlexSendMessage( alt_text= '書籍已查詢完畢!', contents = Bubble.make_carousel(bubble) )
            line_bot_api.reply_message( event.reply_token, msg )
        elif "done" == data.query_result.parameters :
            line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "已完成查詢，如欲再次查詢，請點選常用路線即可。" ) )
            
        elif "more_itinerary" in data.query_result.parameters:
            msg = []
            collection = db['剩餘行程資訊']
            
            res = collection.find_one({'UserID' : event.source.user_id}) 
            print(res['起點座標'],res['終點座標'],res['查詢梯次'])
            itinerary = Get_bus_min_distance.Get_min_distance(res['起點座標'],res['終點座標'],res['查詢梯次'])
            if collection.find_one({ 'UserID' : event.source.user_id}) != None:
                collection.update_one({ 'UserID' : event.source.user_id},{'$set':{'起點座標':res['起點座標'],'終點座標': res['終點座標'],'查詢梯次':res['查詢梯次']+3}})
            else:
                collection.insert_one({ 'UserID' : event.source.user_id,'起點座標':res['起點座標'],'終點座標': res['終點座標'],'查詢梯次':res['查詢梯次']+3})
            print('有',len(itinerary.origin_station),'站')
            bubble = []
            #先將所有資訊個別做成bubble
            for i in range(len(itinerary.route_name)):
                bubble.append(Bubble.Bubble_mid_distance(itinerary,i))
            #再將所有bubble做成carousel後製成flex_message
            if len(bubble) > 10:
                bubble = bubble[:10]
            msg = FlexSendMessage( alt_text= '行程方案已計算完!', contents = Bubble.make_carousel(bubble) )
            reply_list = []
            reply_list.append(msg)
            if len(bubble) == 3:
                quick_reply_list = []
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='更多行程方案', text='@更多行程方案')) )
                reply_list.append( TextSendMessage( text='需要更多行程方案嗎?', quick_reply=QuickReply(items=quick_reply_list) ) )
            if len(itinerary.origin_station) != 0 :
                line_bot_api.reply_message( event.reply_token, reply_list  )
            else:
                line_bot_api.reply_message( event.reply_token, TextSendMessage(text='無法直達')  )
            return 1
        elif 'more_station' in data.query_result.parameters:
            collection = db['剩餘最近公車站']
            location = collection.find_one({'UserID' : event.source.user_id}) 
            station,result,log_lat = bus.bus_Nearest(location['座標'][0],location['座標'][1],location['批次'])
            if collection.find_one({ 'UserID' : event.source.user_id}) != None:
                collection.update_one({'UserID' : event.source.user_id},{'$set':{'座標':[location['座標'][0],location['座標'][1]],'批次':location['批次']+1}})
            else:
                collection.insert_one({'UserID' : event.source.user_id,'座標':[location['座標'][0],location['座標'][1]],'批次':location['批次']+1})
            print(result)
            body = []
            btn = []
            bubble = []
            for j in range(len(result)):
                body = []
                btn = []
                btn.append(Bubble.btn(log_lat[j]))
                for i in range(len(result[j][1])):
                    body.append(Bubble.make_bus_body_tittle('路線:'+str(result[j][1][i][0])+'往('+result[j][1][i][2]+')'))
                    body.append(Bubble.make_bus_body(result[j][1][i][1]))
                if len(result[j][1]) != 0:
                    bubble.append(Bubble.Bubble_bus('站名:'+result[j][0],'即時公車資訊',body,btn,'#5CADAD'))
            msg = FlexSendMessage(alt_text= '公車已查詢完畢!', contents = Bubble.make_carousel(bubble)  )
            reply_list = []
            reply_list.append(msg)
            if len(bubble) == 1:
                quick_reply_list = []
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='更多車站', text='@更多車站')) )
                reply_list.append( TextSendMessage( text='需要更多車站嗎?', quick_reply=QuickReply(items=quick_reply_list) ) )
            else:
                reply_list.append( TextSendMessage( text='已完成查詢，如欲再次查詢，請點選常用路線即可。' ) )        

            line_bot_api.reply_message( event.reply_token, reply_list  )
            return 1
# --------------------------------------------------交通和書籍功能-----------------------------------------------

# --------------------------------------------------餐廳功能-----------------------------------------------
        # elif 'restaurant_recommand' in data.query_result.parameters :
        #     reply_arr = []
        #     quick_reply_list = []
        #     quick_reply_list.append( QuickReplyButton(action=MessageAction(label='萌萌幫你隨機挑', text='萌萌幫我選')) )
        #     quick_reply_list.append( QuickReplyButton(action=MessageAction(label='選口味', text='要甚麼口味呢')) )
        #     quick_reply_list.append( QuickReplyButton(action=MessageAction(label='查看餐廳細項', text='我來想想有什麼餐廳')) )
        #     reply_arr.append( TextSendMessage( text='請選擇一個服務!萌萌會盡全力幫助你喔!', quick_reply=QuickReply(items=quick_reply_list) ) )
        #     line_bot_api.reply_message( event.reply_token, reply_arr )
        # elif '請輸入想查看的餐廳名稱' == data.query_result.fulfillment_text:
        #     line_bot_api.reply_message( event.reply_token, TextSendMessage( text = '請輸入想查看的餐廳名稱' ) )
        # elif 'restaurant_name' in data.query_result.parameters : #查詢特定餐廳的資料
        #     restaurant_name = data.query_result.parameters['restaurant_name']
        #     specific_restaurant = db['specific_restaurant']
        #     temp = specific_restaurant.find_one({'使用者ID': event.source.user_id,'餐廳序號':1})
        #     if temp == None:
        #         specific_restaurant.insert_one({'使用者ID': event.source.user_id,'餐廳序號':1,'餐廳代碼':restaurant_name})
        #     else :
        #         specific_restaurant.update_one({'使用者ID': event.source.user_id,'餐廳序號':1},{'$set':{'餐廳代碼':restaurant_name}})
            

        #     reply_arr = []
        #     quick_reply_list = []
        #     quick_reply_list.append( QuickReplyButton(action=MessageAction(label='店家忙不忙', text='店家忙不忙')) )
        #     quick_reply_list.append( QuickReplyButton(action=MessageAction(label='營業時間', text='營業時間')) )
        #     quick_reply_list.append( QuickReplyButton(action=MessageAction(label='菜單', text='我想看菜單')) )
        #     quick_reply_list.append( QuickReplyButton(action=MessageAction(label='結束', text='不用了謝謝')) )
        #     reply_arr.append( TextSendMessage( text='要查看哪個細項呢~', quick_reply=QuickReply(items=quick_reply_list) ) )
        #     line_bot_api.reply_message( event.reply_token, reply_arr )

        elif 'is_busy' in data.query_result.parameters :
            
            restaurant_code_db = db['total_restaurant_code']
            restaurant_name = db['specific_restaurant']
            save_restaurant_name = restaurant_name.find_one({'使用者ID': event.source.user_id,'餐廳序號':1})
            temp = restaurant_code_db.find_one({'餐廳名稱': {'$regex': save_restaurant_name['餐廳代碼']}}) #匹配到部分相同字串(避免多家分店時搜尋困難)
            if temp == None :
                output = Restaurant.is__busy(save_restaurant_name['餐廳代碼'])
            else :
                output = Restaurant.is__busy(temp['餐廳代碼'])

            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='菜單', text='我想看菜單')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='營業時間', text='營業時間')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='結束', text='不用了謝謝')) )
            reply_arr.append( TextSendMessage( text=output, quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
        elif 'menu_search' in data.query_result.parameters :
            print('這裡是menu_search')
            restaurant_code_db = db['total_restaurant_code']
            restaurant_name = db['specific_restaurant']
            save_restaurant_name = restaurant_name.find_one({'使用者ID': event.source.user_id,'餐廳序號':1})
            temp = restaurant_code_db.find_one({'餐廳名稱': {'$regex': save_restaurant_name['餐廳代碼']}}) #匹配到部分相同字串(避免多家分店時搜尋困難)
            if temp == None :
                output = Restaurant.findMenu(save_restaurant_name['餐廳代碼'])
            else :
                output = Restaurant.findMenu(temp['餐廳代碼'])


            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='店家忙不忙', text='店家忙不忙')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='營業時間', text='營業時間')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='結束', text='不用了謝謝')) )


            temp = []
            temp = output.split('\n')
            temp2 = []
            temp3 = []
            i = 0
            stuff = 1
            word_sum = 0
            flex_num = 0
            while ( i < len(temp) ) and ( word_sum < 2500 ) and stuff < 60:
                if (i-1) == 0 or (i-1)%3 == 0 :
                    
                    i = i + 1

                if (i == 0 or i%3 == 0) and ( i != len( temp ) -1 ) :
                    price = '$' + str(temp[i+1])
                    print('stuff',stuff)
                    stuff += 1 
                else :
                    price = ''

                print(word_sum,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

                temp2.append(Bubble.card2_menu_content(temp[i],i+1,price))
                word_sum = word_sum + len(temp[i])
                flex_num +=1
                print(flex_num,'卡片式: 名稱',temp[i],'價格',price)
                i += 1

            if ( word_sum >= 2500 ) or stuff >= 60 :
                stuff = 1
                word_sum = 0
                while ( i < len(temp) ) and ( word_sum < 2500 ) and stuff < 60 :
                    if (i-1) == 0 or (i-1)%3 == 0 :
                        
                        i = i + 1

                    if (i == 0 or i%3 == 0) and ( i != len( temp ) -1 ) :
                        price = '$' + str(temp[i+1])
                        print('stuff',stuff)
                        stuff += 1 
                    else :
                        price = ''

                    print(word_sum,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

                    temp3.append(Bubble.card2_menu_content(temp[i],i+1,price))
                    word_sum = word_sum + len(temp[i])
                    flex_num +=1
                    print(flex_num,'卡片式: 名稱',temp[i],'價格',price)
                    i += 1
                print(temp,'!!@@')
                card_test = Bubble.card2(temp2,'Menu')
                card_menu = FlexSendMessage( alt_text='快點看訊息拉!', contents = card_test )
                card_test = Bubble.card2(temp3,'Menu')
                card_menu2 = FlexSendMessage( alt_text='快點看訊息拉!', contents = card_test )
                result = []
                result.append(card_menu)
                result.append(card_menu2)
                result.append(TextSendMessage( text='還有甚麼想查看的嗎!', quick_reply=QuickReply(items=quick_reply_list) ))
                line_bot_api.reply_message( event.reply_token, result )
            else :
                print(temp,'!!@@')
                card_test = Bubble.card2(temp2,'Menu')
                card_menu = FlexSendMessage( alt_text='快點看訊息拉!', contents = card_test )
                result = []
                result.append(card_menu)
                result.append(TextSendMessage( text='還有甚麼想查看的嗎!', quick_reply=QuickReply(items=quick_reply_list) ))
                line_bot_api.reply_message( event.reply_token, result )

        elif 'opening_time' in data.query_result.parameters :
            restaurant_code_db = db['total_restaurant_code']
            restaurant_name = db['specific_restaurant']
            save_restaurant_name = restaurant_name.find_one({'使用者ID': event.source.user_id,'餐廳序號':1})
            temp = restaurant_code_db.find_one({'餐廳名稱': {'$regex': save_restaurant_name['餐廳代碼']}}) #匹配到部分相同字串(避免多家分店時搜尋困難)
            if temp == None :
                output = Restaurant.findOpeningTime(save_restaurant_name['餐廳代碼'])
            else :
                output = Restaurant.findOpeningTime(temp['餐廳代碼'])

            temp = []
            temp = output.split('\n')
            temp2 = []
            i = 0
            while i+1 < len(temp):
                temp2.append(Bubble.card2_time_content(temp[i],temp[i+1]))
                i += 2

            
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='店家忙不忙', text='店家忙不忙')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='菜單', text='我想看菜單')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='結束', text='不用了謝謝')) )
            
            card_test = Bubble.card2(temp2,'Opening_Time')
            card_menu = FlexSendMessage( alt_text='快點看訊息拉!', contents = card_test )

            result = []
            result.append(card_menu)
            result.append(TextSendMessage( text='還有甚麼想查看的嗎!', quick_reply=QuickReply(items=quick_reply_list) ))
            line_bot_api.reply_message( event.reply_token, result )
        elif 'Restaurant_change' in data.query_result.parameters :
            code_save2 = db['code_save2']
            code_save = db['code_save']

            i = 0
            output = []
            restaurant = ''
            while i < 3 :
                restaurant_code = code_save2.find_one({'使用者ID': event.source.user_id,'餐廳序號':i+1})
                code_save.update_one({'使用者ID': event.source.user_id,'餐廳序號': i+1} ,{ "$set" : { '餐廳代碼' : restaurant_code['餐廳代碼'] } })
                restaurant += Restaurant.restaurant_change(restaurant_code['餐廳代碼'])
                i += 1

            output = restaurant.split('\n')
            reply = []
            shop1 = output[0]
            shop2 = output[5]
            shop3 = output[10]
            if len(shop1) >= 20 :
                shop1 = output[0][:19]
            if len(shop2) >= 20 :
                shop2 = output[5][:19]
            if len(shop3) >= 20 :
                shop3 = output[10][:19]    
            reply.append( QuickReplyButton(action=MessageAction(label=shop1, text = '第一家')) )
            reply.append( QuickReplyButton(action=MessageAction(label=shop2, text = '第二家')) )
            reply.append( QuickReplyButton(action=MessageAction(label=shop3, text = '第三家')) )
            
            #卡片是訊息測試
            text = []
            card_list = []
            card_list.append(Bubble.card(output[0],output[1],output[2],output[3],output[4]))
            card_list.append(Bubble.card(output[5],output[6],output[7],output[8],output[9]))
            card_list.append(Bubble.card(output[10],output[11],output[12],output[13],output[14]))
            card_output = Bubble.carousel_restaurant(card_list)
            result = FlexSendMessage( alt_text='快點看訊息拉!', contents = card_output )
            text.append(result)
            text.append( TextSendMessage( text='選一家有興趣的吧!', quick_reply=QuickReply(items=reply) ) )
            line_bot_api.reply_message( event.reply_token, text )

        elif 'Restaurant_stop' in data.query_result.parameters :
            line_bot_api.reply_message( event.reply_token, TextSendMessage( text = '好的!隨時再呼喚我!' ) )

        elif 'taste_select' in data.query_result.parameters :
            line_bot_api.reply_message( event.reply_token, TextSendMessage( text = data.query_result.fulfillment_text ) )

        elif 'restaurant_random' in data.query_result.parameters :
            food = randomTaste.randomRestaurant()
            restaurant = Restaurant.findRestaurant(food)
            code_save = db['code_save']
            code_save2 = db['code_save2']
            output = []
            output = restaurant[0].split('\n')
            i = 0
            temp = code_save.find_one({'使用者ID': event.source.user_id,'餐廳序號': 1})
            while i < 3 :
                if temp == None :
                    code_save.insert_one({'使用者ID': event.source.user_id,'餐廳序號': i+1 ,'餐廳代碼': restaurant[1][i]})
                    i += 1
                else :
                    code_save.update_one({'使用者ID': event.source.user_id,'餐廳序號': i+1} ,{ "$set" : {'餐廳代碼' : restaurant[1][i] } })
                    i += 1
                    

            j = 0
            temp = code_save2.find_one({'使用者ID': event.source.user_id,'餐廳序號': 1})
            while j < 3 :
                if temp == None :
                    code_save2.insert_one({'使用者ID': event.source.user_id,'餐廳序號': j+1 ,'餐廳代碼': restaurant[1][j+3]})
                    j += 1
                else :
                    code_save2.update_one({'使用者ID': event.source.user_id,'餐廳序號': j+1} ,{ "$set" : { '餐廳代碼': restaurant[1][j+3] } })
                    j += 1

            reply = []
            shop1 = output[0]
            shop2 = output[5]
            shop3 = output[10]
            if len(shop1) >= 20 :
                shop1 = output[0][:19]
            if len(shop2) >= 20 :
                shop2 = output[5][:19]
            if len(shop3) >= 20 :
                shop3 = output[10][:19]    
            reply.append( QuickReplyButton(action=MessageAction(label=shop1, text = '第一家')) )
            reply.append( QuickReplyButton(action=MessageAction(label=shop2, text = '第二家')) )
            reply.append( QuickReplyButton(action=MessageAction(label=shop3, text = '第三家')) )
            reply.append( QuickReplyButton(action=MessageAction(label='換一批', text = '換一批')) )
            
            #卡片是訊息測試
            text = []
            card_list = []
            card_list.append(Bubble.card(output[0],output[1],output[2],output[3],output[4]))#卡片1
            card_list.append(Bubble.card(output[5],output[6],output[7],output[8],output[9]))#卡片2
            card_list.append(Bubble.card(output[10],output[11],output[12],output[13],output[14]))#卡片3
            card_output = Bubble.carousel_restaurant(card_list)#三合一卡片
            result = FlexSendMessage( alt_text='快點看訊息拉!', contents = card_output )#卡片輸出內容
            text.append(result)
            text.append( TextSendMessage( text='選一家有興趣的吧!', quick_reply=QuickReply(items=reply) ) )
            line_bot_api.reply_message( event.reply_token, text )

        elif 'taste' in data.query_result.parameters : 
            taste = data.query_result.parameters['taste']
            food = randomTaste.likelyTaste(taste)
            restaurant = Restaurant.findRestaurant(food)
            code_save = db['code_save']
            code_save2 = db['code_save2']
            output = []
            output = restaurant[0].split('\n')
            i = 0
            temp = code_save.find_one({'使用者ID': event.source.user_id,'餐廳序號': 1})
            while i < 3 :
                if temp == None :
                    code_save.insert_one({'使用者ID': event.source.user_id,'餐廳序號': i+1 ,'餐廳代碼': restaurant[1][i]})
                    i += 1
                else :
                    code_save.update_one({'使用者ID': event.source.user_id,'餐廳序號': i+1} ,{ "$set" : {'餐廳代碼' : restaurant[1][i] } })
                    i += 1
                    

            j = 0
            temp = code_save2.find_one({'使用者ID': event.source.user_id,'餐廳序號': 1})
            while j < 3 :
                if temp == None :
                    code_save2.insert_one({'使用者ID': event.source.user_id,'餐廳序號': j+1 ,'餐廳代碼': restaurant[1][j+3]})
                    j += 1
                else :
                    code_save2.update_one({'使用者ID': event.source.user_id,'餐廳序號': j+1} ,{ "$set" : { '餐廳代碼': restaurant[1][j+3] } })
                    j += 1

            reply = []
            shop1 = output[0]
            shop2 = output[5]
            shop3 = output[10]
            if len(shop1) >= 20 :
                shop1 = output[0][:19]
            if len(shop2) >= 20 :
                shop2 = output[5][:19]
            if len(shop3) >= 20 :
                shop3 = output[10][:19]    
            reply.append( QuickReplyButton(action=MessageAction(label=shop1, text = '第一家')) )
            reply.append( QuickReplyButton(action=MessageAction(label=shop2, text = '第二家')) )
            reply.append( QuickReplyButton(action=MessageAction(label=shop3, text = '第三家')) )
            reply.append( QuickReplyButton(action=MessageAction(label='換一批', text = '換一批')) )
            
            #卡片是訊息測試
            print(restaurant[0])
            text = []
            card_list = []
            card_list.append(Bubble.card(output[0],output[1],output[2],output[3],output[4]))
            card_list.append(Bubble.card(output[5],output[6],output[7],output[8],output[9]))
            card_list.append(Bubble.card(output[10],output[11],output[12],output[13],output[14]))
            card_output = Bubble.carousel_restaurant(card_list)
            result = FlexSendMessage( alt_text='快點看訊息拉!', contents = card_output )
            text.append(result)
            text.append( TextSendMessage( text='選一家有興趣的吧!', quick_reply=QuickReply(items=reply) ) )
            line_bot_api.reply_message( event.reply_token, text )

        elif 'restaurant' in data.query_result.parameters  : #找餐廳
            restaurant = ""
            food = data.query_result.parameters['restaurant']
            restaurant = Restaurant.findRestaurant(food)
            code_save = db['code_save']
            code_save2 = db['code_save2']

            output = []
            output = restaurant[0].split('\n')

            i = 0
            temp = code_save.find_one({'使用者ID': event.source.user_id,'餐廳序號': 1})
            while i < 3 :
                if temp == None :
                    code_save.insert_one({'使用者ID': event.source.user_id,'餐廳序號': i+1 ,'餐廳代碼': restaurant[1][i]})
                    i += 1
                else :
                    code_save.update_one({'使用者ID': event.source.user_id,'餐廳序號': i+1} ,{ "$set" : {'餐廳代碼' : restaurant[1][i] } })
                    i += 1
                    

            j = 0
            temp = code_save2.find_one({'使用者ID': event.source.user_id,'餐廳序號': 1})
            while j < 3 :
                if temp == None :
                    code_save2.insert_one({'使用者ID': event.source.user_id,'餐廳序號': j+1 ,'餐廳代碼': restaurant[1][j+3]})
                    j += 1
                else :
                    code_save2.update_one({'使用者ID': event.source.user_id,'餐廳序號': j+1} ,{ "$set" : { '餐廳代碼': restaurant[1][j+3] } })
                    j += 1

            reply = []
            
            shop1 = output[0]
            shop2 = output[5]
            shop3 = output[10]
            if len(shop1) >= 20 :
                shop1 = output[0][:19]
            if len(shop2) >= 20 :
                shop2 = output[5][:19]
            if len(shop3) >= 20 :
                shop3 = output[10][:19]    
            reply.append( QuickReplyButton(action=MessageAction(label=shop1, text = '第一家')) )
            reply.append( QuickReplyButton(action=MessageAction(label=shop2, text = '第二家')) )
            reply.append( QuickReplyButton(action=MessageAction(label=shop3, text = '第三家')) )
            reply.append( QuickReplyButton(action=MessageAction(label='換一批', text = '換一批')) )
            
            #卡片是訊息測試
            text = []
            card_list = []
            card_list.append(Bubble.card(output[0],output[1],output[2],output[3],output[4]))
            card_list.append(Bubble.card(output[5],output[6],output[7],output[8],output[9]))
            card_list.append(Bubble.card(output[10],output[11],output[12],output[13],output[14]))
            card_output = Bubble.carousel_restaurant(card_list)
            result = FlexSendMessage( alt_text='快點看訊息拉!', contents = card_output )
            text.append(result)
            text.append( TextSendMessage( text='選一家有興趣的吧!', quick_reply=QuickReply(items=reply) ) )
            line_bot_api.reply_message( event.reply_token, text )
            
            #卡片是訊息測試結束
            
        elif 'Restaurant_select' in data.query_result.parameters  : #選擇哪一家的菜單
            input = ''
            input = data.query_result.parameters['Restaurant_select']

            db_code = ''
            code_save = db['code_save']
            if(input == '第一家'): 
                db_code = code_save.find_one({'使用者ID': event.source.user_id,'餐廳序號':1})
            elif(input == '第二家'):
                db_code = code_save.find_one({'使用者ID': event.source.user_id,'餐廳序號':2})
            elif(input == '第三家'):
                db_code = code_save.find_one({'使用者ID': event.source.user_id,'餐廳序號':3})
                
            
            specific_restaurant = db['specific_restaurant']
            temp = specific_restaurant.find_one({'使用者ID': event.source.user_id,'餐廳序號':1})
            if temp == None:
                specific_restaurant.insert_one({'使用者ID': event.source.user_id,'餐廳序號':1,'餐廳代碼':db_code['餐廳代碼']})
            else :
                specific_restaurant.update_one({'使用者ID': event.source.user_id,'餐廳序號':1},{'$set':{'餐廳代碼':db_code['餐廳代碼']}})

            reply_arr = []
            quick_reply_list = []
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='店家忙不忙', text='店家忙不忙')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='營業時間', text='營業時間')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='菜單', text='我想看菜單')) )
            quick_reply_list.append( QuickReplyButton(action=MessageAction(label='結束', text='不用了謝謝')) )
            reply_arr.append( TextSendMessage( text='要查看哪個細項呢~', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )

        else :
            print("啥都沒進去")
            return 2
    
        
    elif event.message.type == 'location':
        if "@reply_itinerary_1" == data.query_result.fulfillment_text:
            collection = db['位置']
            location = collection.find_one({'UserID' : event.source.user_id}) 
            # collection.delete_one({'UserID' : event.source.user_id}) 
            collection = db['起點']
            if collection.find_one({'UserID' : event.source.user_id}) != None:
                collection.update_one({'UserID' : event.source.user_id},{'$set':{'座標' : location['座標'],"Date" : datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')}})
            else:
                collection.insert_one({'UserID' : event.source.user_id,'座標' : location['座標'],"Date" : datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')})
            quick_reply_list = []
            reply_arr = []
            quick_reply_list.append( QuickReplyButton(action=LocationAction(label='輸入終點')) )
            reply_arr.append( TextSendMessage( text='請輸入終點', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_arr )
            # 步行距離1、起點車站、搭乘路線、公車時間、經過站數、終點車站、步行距離2、目的地(預計取消:使用line只能獲取座標)
            return 1 #[24.953612, 121.230613] to [24.95747, 121.240846]
        elif "@reply_itinerary_2" == data.query_result.fulfillment_text:
            collection = db['功能使用狀況']
            temp = collection.find_one({ '功能名稱': '行程結束'})
            if temp != None:
                collection.update_one({ '功能名稱': '行程結束' },{'$set':{'使用次數':temp['使用次數']+1}})
            else:
                collection.insert_one({ '功能名稱': '行程結束','使用次數':1 })

            msg = []
            collection1 = db['起點']
            origin_location = collection1.find_one({'UserID' : event.source.user_id}) 
            collection1.delete_one({'UserID' : event.source.user_id}) 
            #終點
            collection = db['位置']
            destination_location = collection.find_one({'UserID' : event.source.user_id})
            # collection.delete_one({'UserID' : event.source.user_id}) 

            reply_arr = []
            print(origin_location['座標'],end='')
            print('to',destination_location['座標'])
            itinerary = Get_bus_min_distance.Get_min_distance(origin_location['座標'],destination_location['座標'],0)
            collection = db['剩餘行程資訊']
            if collection.find_one({ 'UserID' : event.source.user_id}) != None:
                collection.update_one({ 'UserID' : event.source.user_id},{'$set':{'起點座標':origin_location['座標'],'終點座標': destination_location['座標'],'查詢梯次':3}})
            else:
                collection.insert_one({ 'UserID' : event.source.user_id,'起點座標':origin_location['座標'],'終點座標': destination_location['座標'],'查詢梯次':3})
            print('有',len(itinerary.origin_station),'站')
            bubble = []
            #先將所有資訊個別做成bubble
            for i in range(len(itinerary.route_name)):
                bubble.append(Bubble.Bubble_mid_distance(itinerary,i))
            #再將所有bubble做成carousel後製成flex_message
            msg = FlexSendMessage( alt_text= '行程方案已計算完!', contents = Bubble.make_carousel(bubble) )
            reply_list = []
            reply_list.append(msg)
            if len(bubble) == 3:
                quick_reply_list = []
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='更多行程方案', text='@更多行程方案')) )
                reply_list.append( TextSendMessage( text='需要更多行程方案嗎?', quick_reply=QuickReply(items=quick_reply_list) ) )
            if len(itinerary.origin_station) != 0 :
                line_bot_api.reply_message( event.reply_token, reply_list  )
            else:
                line_bot_api.reply_message( event.reply_token, TextSendMessage(text='目前無法抵達')  )
            return 1
        elif '@reply_bus_Nearest_1' == data.query_result.fulfillment_text:
            collection = db['功能使用狀況']
            temp = collection.find_one({ '功能名稱': '最近公車結束'})
            if temp != None:
                collection.update_one({ '功能名稱': '最近公車結束' },{'$set':{'使用次數':temp['使用次數']+1}})
            else:
                collection.insert_one({ '功能名稱': '最近公車結束','使用次數':1 })

            collection = db['位置']
            location = collection.find_one({'UserID' : event.source.user_id}) 
            # collection.delete_one({'UserID' : event.source.user_id}) 
            station,result,log_lat = bus.bus_Nearest(location['座標'][0],location['座標'][1],0)

            collection = db['剩餘最近公車站']
            if collection.find_one({ 'UserID' : event.source.user_id}) != None:
                collection.update_one({'UserID' : event.source.user_id},{'$set':{'座標':[location['座標'][0],location['座標'][1]],'批次':1}})
            else:
                collection.insert_one({'UserID' : event.source.user_id,'座標':[location['座標'][0],location['座標'][1]],'批次':1})
            print(result)
            body = []
            btn = []
            bubble = []
            for j in range(len(result)):
                body = []
                btn = []
                btn.append(Bubble.btn(log_lat[j]))
                for i in range(len(result[j][1])):
                    body.append(Bubble.make_bus_body_tittle('路線:'+str(result[j][1][i][0])+'往('+result[j][1][i][2]+')'))
                    body.append(Bubble.make_bus_body(result[j][1][i][1]))
                if len(result[j][1]) != 0:
                    bubble.append(Bubble.Bubble_bus('站名:'+result[j][0],'即時公車資訊',body,btn,'#5CADAD'))
            msg = FlexSendMessage(alt_text= '公車已查詢完畢!', contents = Bubble.make_carousel(bubble)  )
            reply_list = []
            reply_list.append(msg)
            if len(bubble) == 1:
                quick_reply_list = []
                quick_reply_list.append( QuickReplyButton(action=MessageAction(label='更多車站', text='@更多車站')) )
                reply_list.append( TextSendMessage( text='需要更多車站嗎?', quick_reply=QuickReply(items=quick_reply_list) ) )
            line_bot_api.reply_message( event.reply_token, reply_list  )
            return 1
        else :
            print("啥都沒進去")
            return 2
if __name__ == "__main__":
    app.run()
