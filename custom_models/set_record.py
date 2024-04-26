import urllib
import re


def prepare_record(event):
    user_id = event.source.user_id
    user_msg = event.message.text
    record_list = [str(user_id), user_msg]  
    return record_list

def prepare_location_record(event):
    user_id = event.source.user_id
    user_log = event.message.longitude
    user_lat = event.message.latitude
    user_loc = [user_lat,user_log]
    record_list = [str(user_id), user_loc]  
    return record_list
    
def prepare_time_record(event):
    user_id = event.source.user_id
    user_train_time = event.postback.params['datetime']
    record_list = [str(user_id), user_train_time]  
    return record_list




