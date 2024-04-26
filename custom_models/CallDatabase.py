import psycopg2
import os
import pymongo
from datetime import datetime
import pytz
from custom_models import config
def line_insert_record(record_list):
    client = pymongo.MongoClient(config.MONGO_DB)
    db = client.User_Message 
    collection = db[record_list[0]]
    time =  datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')
    msg  = {"Msg" : record_list[1], "Date" :time}
    collection.insert_one(msg)
    print( "成功匯入文字資訊囉" ) 
    return time
    
def line_insert_location(record_list):
    client = pymongo.MongoClient(config.MONGO_DB)
    db = client.test
    collection = db['位置']
    if collection.find_one({ 'UserID' : record_list[0]}) != None:
        collection.update_one({ 'UserID' : record_list[0]},{'$set':{ '座標' : record_list[1],"Date" : datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')}})
    else:
        collection.insert_one({ 'UserID' : record_list[0],'座標' : record_list[1],"Date" : datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')})
    print( "成功匯入位置資訊囉" ) 
    return 1

def line_insert_time(record_list):
    client = pymongo.MongoClient(config.MONGO_DB)
    db = client.test
    collection = db['時間']
    try:
        query = { 'UserID' : record_list[0]}
        collection.delete_one(query)
        query = { 'UserID' : record_list[0], '時間' : record_list[1],"Date" : datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S') }
        collection.insert_one(query)
    except:
        query = { 'UserID' : record_list[0], '時間' : record_list[1],"Date" : datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S') }
        collection.insert_one(query)
    print( "成功匯入時間資訊囉" ) 
    return 1

    