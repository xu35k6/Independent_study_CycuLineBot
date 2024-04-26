import pymongo
import random
from custom_models import convert_to_image, make_flex_message


def Add_condition( db, id, class_time, class_name, class_type ) : # 排課程的條件
    collection = db['暫存排課條件']
    data = collection.find_one({ 'UserID' : id },{ "_id" : 0 })

    if data != None : # 有說過條件
        for t in class_time :
            data['時間'].append( t )
        for name in class_name : # 有說課程名稱 
            data['課程名稱'].append( name )
        for type in class_type : # 有說課程名稱 
            data['課程類別'].append( type )
        collection.update_one({ 'UserID' : id },{ "$set": { '時間' : data['時間'], '課程名稱' : data['課程名稱'], '課程類別' : data['課程類別'] } })

    else : # 把這次的條件存起來
        time_list = []
        class_list = []
        type_list = []
        for name in class_name : 
            class_list.append( name )
        for t in class_time :
            time_list.append( t )
        for t in class_type :
            type_list.append( t )
        query = { 'UserID' : id, '時間' : time_list, '課程名稱' : class_list, '課程類別' : type_list }
        collection.insert_one( query )

def Find_Empty_time( data ) : # 找空堂壓
    time = []
    empty_list = []

    time.extend( [ '時段A', '時段1', '時段2', '時段3', '時段4', '時段B', '時段5', '時段6', '時段7', '時段8', '時段C', '時段D', '時段E', '時段F', '時段G' ] )
    i = 0
    while i < 7 :
        empty_str = "" # 存空堂的節數
        for t in time :
            if data[t][i] == " " : # 空堂GET
                empty_str = empty_str + t[-1]
        empty_list.append( empty_str )
        i = i + 1
    return empty_list



def Find_Cond_and_Add_Course( db, id ) : # 當使用者前面已經輸入過條件後要加課
    collection_cond = db['暫存排課條件']
    collection_table = db['class_table']
    collection_data = db['classdata_1111']
    cond = collection_cond.find_one( { 'UserID' : id },{ "_id" : 0 } )
    result = []
    if cond != None : # 有東西
        time_list = cond['時間']
        class_name_list = cond['課程名稱']
        class_type_list = cond['課程類別']
        if time_list : # 條件裡面有給時間
            if class_type_list : # 使用者有選類別&時間
                if class_name_list : # 使用者有給課程名稱&類別&時間
                    for t in time_list : # 不是空的list就會進去 使用者有給時間
                        day = t[0] # 禮拜幾
                        time = t[1] # 第幾節
                        i = 0
                        index = 0
                        while index < len( class_type_list ) :
                            type = class_type_list[index]
                            while i < len( class_name_list ) : 
                                query = day + "-"
                                class_name = class_name_list[i]
                                data = collection_data.find({ '$or' : [{'時間1' : { '$regex': query }}, {'時間2' : { '$regex': query }}, {'時間3' : { '$regex': query }}], '課程名稱' : { '$regex': class_name }, '身分' : "大學部", "類別" : type },{ "_id" : 0 } )
                                for d in data :
                                    temp = []
                                    if d['時間1'][2:] in time : # 這節課的時間有在使用者所給的空堂時間裡
                                        if d['時間2'] == 'nan' : # 沒時間2
                                            if d['教室1'] == 'nan' :
                                                d['教室1'] = ""
                                            temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['課程代碼'] ] )  
                                        elif d['時間3'] == 'nan' : # 沒時間3
                                            if d['教室1'] == 'nan' :
                                                d['教室1'] = ""
                                            if d['教室2'] == 'nan' :
                                                d['教室2'] = ""
                                            temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['課程代碼'] ] )  
                                        else :
                                            if d['教室1'] == 'nan' :
                                                d['教室1'] = ""
                                            if d['教室2'] == 'nan' :
                                                d['教室2'] = ""
                                            if d['教室3'] == 'nan' :
                                                d['教室3'] = ""
                                            temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['時間3'], d['教室3'], d['課程代碼'] ] )  
                                        if temp : # temp有東西
                                            result.append( temp.copy() )
                                i = i + 1
                            index = index + 1  
                else : # 使用者只有給時間跟類別
                    for t in time_list : # 不是空的list就會進去 使用者有給時間
                        day = t[0] # 禮拜幾
                        time = t[1] # 第幾節
                        query = day + "-"
                        index = 0
                        while index < len( class_type_list ) :
                            type = class_type_list[index]
                            data = collection_data.find({ '$or' : [{'時間1' : { '$regex': query }}, {'時間2' : { '$regex': query }}, {'時間3' : { '$regex': query }}], '身分' : "大學部", "類別" : type },{ "_id" : 0 } )
                            for d in data :
                                temp = []
                                if d['時間1'][2:] in time : # 這節課的時間有在使用者所給的空堂時間裡
                                    if d['時間2'] == 'nan' : # 沒時間2
                                        if d['教室1'] == 'nan' :
                                            d['教室1'] = ""
                                        temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['課程代碼'] ] )  
                                    elif d['時間3'] == 'nan' : # 沒時間3
                                        if d['教室1'] == 'nan' :
                                            d['教室1'] = ""
                                        if d['教室2'] == 'nan' :
                                            d['教室2'] = ""
                                        temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['課程代碼'] ] )  
                                    else :
                                        if d['教室1'] == 'nan' :
                                            d['教室1'] = ""
                                        if d['教室2'] == 'nan' :
                                            d['教室2'] = ""
                                        if d['教室3'] == 'nan' :
                                            d['教室3'] = ""
                                        temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['時間3'], d['教室3'], d['課程代碼'] ] )  
                                    if temp : # temp有東西
                                        result.append( temp.copy() )  
                            index = index + 1
            elif class_name_list : # 使用者有給課程名稱&時間
                for t in time_list : # 不是空的list就會進去 使用者有給時間
                    day = t[0] # 禮拜幾
                    time = t[1] # 第幾節
                    query = day + "-"
                    while i < len( class_name_list ) : 
                        class_name = class_name_list[i]
                        data = collection_data.find({ '$or' : [{'時間1' : { '$regex': query }}, {'時間2' : { '$regex': query }}, {'時間3' : { '$regex': query }}], '課程名稱' : { '$regex': class_name }, '身分' : "大學部" },{ "_id" : 0 } )
                        for d in data :
                            temp = []
                            if d['時間1'][2:] in time : # 這節課的時間有在使用者所給的空堂時間裡
                                if d['時間2'] == 'nan' : # 沒時間2
                                    if d['教室1'] == 'nan' :
                                        d['教室1'] = ""
                                    temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['課程代碼'] ] )  
                                elif d['時間3'] == 'nan' : # 沒時間3
                                    if d['教室1'] == 'nan' :
                                        d['教室1'] = ""
                                    if d['教室2'] == 'nan' :
                                        d['教室2'] = ""
                                    temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['課程代碼'] ] )  
                                else :
                                    if d['教室1'] == 'nan' :
                                        d['教室1'] = ""
                                    if d['教室2'] == 'nan' :
                                        d['教室2'] = ""
                                    if d['教室3'] == 'nan' :
                                        d['教室3'] = ""
                                    temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['時間3'], d['教室3'], d['課程代碼'] ] )  
                                if temp : # temp有東西
                                    result.append( temp.copy() )
                        i = i + 1
            else : # 只有時間
                for t in time_list : # 不是空的list就會進去 使用者有給時間
                    day = t[0] # 禮拜幾
                    time = t[1] # 第幾節
                    print(t[0])
                    print(t[1])
                    query = day + "-"
                    data = collection_data.find({ '$or' : [{'時間1' : { '$regex': query }}, {'時間2' : { '$regex': query }}, {'時間3' : { '$regex': query }}], '身分' : "大學部" },{ "_id" : 0 } )
                    for d in data :
                        temp = []
                        if d['時間1'][2:] in time : # 這節課的時間有在使用者所給的空堂時間裡
                            if d['時間2'] == 'nan' : # 沒時間2
                                if d['教室1'] == 'nan' :
                                    d['教室1'] = ""
                                temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['課程代碼'] ] )  
                            elif d['時間3'] == 'nan' : # 沒時間3
                                if d['教室1'] == 'nan' :
                                    d['教室1'] = ""
                                if d['教室2'] == 'nan' :
                                    d['教室2'] = ""
                                temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['課程代碼'] ] )  
                            else :
                                if d['教室1'] == 'nan' :
                                    d['教室1'] = ""
                                if d['教室2'] == 'nan' :
                                    d['教室2'] = ""
                                if d['教室3'] == 'nan' :
                                    d['教室3'] = ""
                                temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['時間3'], d['教室3'], d['課程代碼'] ] )  
                            if temp : # temp有東西
                                result.append( temp.copy() )
        elif class_type_list : # 使用者沒給時間但有給課程類別
            if class_name_list : # 使用者有給類別跟課程名稱
                for type in class_type_list : # 使用者有給課程類別
                    user_table = collection_table.find_one( { '名稱' : id },{ "_id" : 0 } )
                    if user_table != None : # 使用者有課表
                        empty_list = Find_Empty_time( user_table ) # 找課表內的空堂時間
                        index = 0
                        while index < len( class_name_list ) :
                            class_name = class_name_list[index]
                            i = 0 
                            while i < 7 :
                                query = str( i + 1 ) + "-"
                                data = collection_data.find({ '$or' : [{'時間1' : { '$regex': query }}, {'時間2' : { '$regex': query }}, {'時間3' : { '$regex': query }}], "類別" : type, "課程名稱" : class_name, '身分' : "大學部" },{ "_id" : 0 } )
                                for d in data :
                                    temp = []
                                    if d['時間1'][0] == str( i + 1 ) and d['時間1'][2:] in empty_list[i] : # 這節課的時間有在使用者所給的空堂時間裡
                                        if d['時間2'] == 'nan' : # 沒時間2
                                            if d['教室1'] == 'nan' :
                                                d['教室1'] = ""
                                            temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['課程代碼'] ] )  
                                        elif d['時間2'][2:] in empty_list[int(d['時間2'][0]) - 1] : # 時間2也符合空堂時間
                                            if d['時間3'] == 'nan' : # 沒時間3
                                                if d['教室1'] == 'nan' :
                                                    d['教室1'] = "" 
                                                if d['教室2'] == 'nan' :
                                                    d['教室2'] = "" 
                                                temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['課程代碼'] ] )  
                                            elif d['時間3'][2:] in empty_list[int(d['時間3'][0]) - 1] : # 時間3也符合空堂時間
                                                if d['教室1'] == 'nan' :
                                                    d['教室1'] = "" 
                                                if d['教室2'] == 'nan' :
                                                    d['教室2'] = ""
                                                if d['教室3'] == 'nan' :
                                                    d['教室3'] = ""    
                                                temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['時間3'], d['教室3'], d['課程代碼'] ] )  
                                    if temp : # temp有東西
                                        result.append( temp.copy() )
                                i = i + 1
                            index = index + 1
                    else : # 使用者沒有課表
                        for type in class_type_list : # 使用者有給課程類別
                            index = 0
                            while index < len( class_name_list ) :
                                class_name = class_name_list[index]
                                data = collection_data.find({ "課程名稱" : class_name, "類別" : type, '身分' : "大學部" },{ "_id" : 0 } )
                                for d in data :
                                    temp = []
                                    if d['時間2'] == 'nan' : # 沒時間2
                                        if d['教室1'] == 'nan' :
                                            d['教室1'] = ""
                                        temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['課程代碼'] ] )  
                                    elif d['時間3'] == 'nan' : # 沒時間3
                                        if d['教室1'] == 'nan' :
                                            d['教室1'] = "" 
                                        if d['教室2'] == 'nan' :
                                            d['教室2'] = ""
                                        temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['課程代碼'] ] )    
                                    else :
                                        if d['教室1'] == 'nan' :
                                            d['教室1'] = "" 
                                        if d['教室2'] == 'nan' :
                                            d['教室2'] = ""
                                        if d['教室3'] == 'nan' :
                                            d['教室3'] = ""  
                                        temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['時間3'], d['教室3'], d['課程代碼'] ] )  
                                    if temp :
                                        result.append( temp.copy() )
            else : # 只有類別
                for type in class_type_list : # 使用者有給課程類別
                    user_table = collection_table.find_one( { '名稱' : id },{ "_id" : 0 } )
                    if user_table != None : # 使用者有課表
                        empty_list = Find_Empty_time( user_table ) # 找課表內的空堂時間
                        i = 0 
                        while i < 7 :
                            query = str( i + 1 ) + "-"
                            data = collection_data.find({ '$or' : [{'時間1' : { '$regex': query }}, {'時間2' : { '$regex': query }}, {'時間3' : { '$regex': query }}], "類別" : type, '身分' : "大學部" },{ "_id" : 0 } )
                            for d in data :
                                temp = []
                                if d['時間1'][0] == str( i + 1 ) and d['時間1'][2:] in empty_list[i] : # 這節課的時間有在使用者所給的空堂時間裡
                                    if d['時間2'] == 'nan' : # 沒時間2
                                        if d['教室1'] == 'nan' :
                                            d['教室1'] = ""
                                        temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['課程代碼'] ] )  
                                    elif d['時間2'][2:] in empty_list[int(d['時間2'][0]) - 1] : # 時間2也符合空堂時間
                                        if d['時間3'] == 'nan' : # 沒時間3
                                            if d['教室1'] == 'nan' :
                                                d['教室1'] = "" 
                                            if d['教室2'] == 'nan' :
                                                d['教室2'] = "" 
                                            temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['課程代碼'] ] )  
                                        elif d['時間3'][2:] in empty_list[int(d['時間3'][0]) - 1] : # 時間3也符合空堂時間
                                            if d['教室1'] == 'nan' :
                                                d['教室1'] = "" 
                                            if d['教室2'] == 'nan' :
                                                d['教室2'] = ""
                                            if d['教室3'] == 'nan' :
                                                d['教室3'] = ""    
                                            temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['時間3'], d['教室3'], d['課程代碼'] ] )  
                                if temp : # temp有東西
                                    result.append( temp.copy() )
                            i = i + 1
                    else : # 使用者沒有課表
                        for type in class_type_list : # 使用者有給課程類別
                            data = collection_data.find({ "類別" : type, '身分' : "大學部" },{ "_id" : 0 } )
                            for d in data :
                                temp = []
                                if d['時間2'] == 'nan' : # 沒時間2
                                    if d['教室1'] == 'nan' :
                                        d['教室1'] = ""
                                    temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['課程代碼'] ] )  
                                elif d['時間3'] == 'nan' : # 沒時間3
                                    if d['教室1'] == 'nan' :
                                        d['教室1'] = "" 
                                    if d['教室2'] == 'nan' :
                                        d['教室2'] = ""
                                    temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['課程代碼'] ] )    
                                else :
                                    if d['教室1'] == 'nan' :
                                        d['教室1'] = "" 
                                    if d['教室2'] == 'nan' :
                                        d['教室2'] = ""
                                    if d['教室3'] == 'nan' :
                                        d['教室3'] = ""  
                                    temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['時間3'], d['教室3'], d['課程代碼'] ] )  
                                if temp :
                                    result.append( temp.copy() )
        else : # 使用者只有給課程名稱
            for class_name in class_name_list : # 使用者有給課程名稱
                user_table = collection_table.find_one( { '名稱' : id },{ "_id" : 0 } )
                if user_table != None : # 使用者有課表
                    empty_list = Find_Empty_time( user_table ) # 找課表內的空堂時間
                    i = 0 
                    while i < 7 :
                        query = str( i + 1 ) + "-"
                        data = collection_data.find({ '$or' : [{'時間1' : { '$regex': query }}, {'時間2' : { '$regex': query }}, {'時間3' : { '$regex': query }}], '課程名稱' : { '$regex': class_name }, '身分' : "大學部" },{ "_id" : 0 } )
                        for d in data :
                            temp = []
                            if d['時間1'][0] == str( i + 1 ) and d['時間1'][2:] in empty_list[i] : # 這節課的時間有在使用者所給的空堂時間裡
                                if d['時間2'] == 'nan' : # 沒時間2
                                    if d['教室1'] == 'nan' :
                                        d['教室1'] = ""
                                    temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['課程代碼'] ] )  
                                elif d['時間2'][2:] in empty_list[int(d['時間2'][0]) - 1] : # 時間2也符合空堂時間
                                    if d['時間3'] == 'nan' : # 沒時間3
                                        if d['教室1'] == 'nan' :
                                            d['教室1'] = "" 
                                        if d['教室2'] == 'nan' :
                                            d['教室2'] = "" 
                                        temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['課程代碼'] ] )  
                                    elif d['時間3'][2:] in empty_list[int(d['時間3'][0]) - 1] : # 時間3也符合空堂時間
                                        if d['教室1'] == 'nan' :
                                            d['教室1'] = "" 
                                        if d['教室2'] == 'nan' :
                                            d['教室2'] = ""
                                        if d['教室3'] == 'nan' :
                                            d['教室3'] = ""    
                                        temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['時間3'], d['教室3'], d['課程代碼'] ] )  
                            if temp : # temp有東西
                                result.append( temp.copy() )
                        i = i + 1
                else : # 使用者沒有課表
                    for class_name in class_name_list : # 使用者有給課程名稱
                        data = collection_data.find({ '課程名稱' : { '$regex': class_name }, '身分' : "大學部" },{ "_id" : 0 } )
                        for d in data :
                            temp = []
                            if d['時間2'] == 'nan' : # 沒時間2
                                if d['教室1'] == 'nan' :
                                    d['教室1'] = ""
                                temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['課程代碼'] ] )  
                            elif d['時間3'] == 'nan' : # 沒時間3
                                if d['教室1'] == 'nan' :
                                    d['教室1'] = "" 
                                if d['教室2'] == 'nan' :
                                    d['教室2'] = ""
                                temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['課程代碼'] ] )    
                            else :
                                if d['教室1'] == 'nan' :
                                    d['教室1'] = "" 
                                if d['教室2'] == 'nan' :
                                    d['教室2'] = ""
                                if d['教室3'] == 'nan' :
                                    d['教室3'] = ""  
                                temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['時間3'], d['教室3'], d['課程代碼'] ] )  
                            if temp :
                                result.append( temp.copy() )
        if len( result ) > 10 : # 超過10個隨機取10個
            number_of_index = []
            i = 0
            while i < len( result ) :
                number_of_index.append( i )
                i = i + 1
            
            index = random.sample( number_of_index, 10 )
            result_list = []
            for i in index :
                result_list.append( result[ i ] )
            result = result_list
        if result : # result 有東西
            content = make_flex_message.make_course_search_flex(result)
        else :
            content = None
        collection_cond.delete_one( { 'UserID' : id } )
        return content
    else :
        return None


def Find_Class_Data( db, id, classData ) : # 單純查課程的時候用
    collection_table = db['class_table']
    user_table = collection_table.find_one( { '名稱' : id },{ "_id" : 0 } )
    result = []
    if user_table != None : # 使用者有課表
        empty_list = Find_Empty_time( user_table ) # 找課表內的空堂時間
        for d in classData :
            temp = []
            if d['時間1'] != "nan" :
                i = int( d['時間1'][0] ) - 1
            if d['時間1'] == "nan" or d['時間1'][2:] in empty_list[i] : # 這節課的時間有在使用者所給的空堂時間裡
                if d['時間2'] == 'nan' : # 沒時間2
                    if d['教室1'] == 'nan' :
                        d['教室1'] = "" 
                    temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['課程代碼'] ] )  
                elif d['時間2'][2:] in empty_list[int(d['時間2'][0]) - 1] : # 時間2也符合空堂時間
                    if d['時間3'] == 'nan' : # 沒時間3
                        if d['教室1'] == 'nan' :
                            d['教室1'] = "" 
                        if d['教室2'] == 'nan' :
                            d['教室2'] = ""  
                        temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['課程代碼'] ] )  
                    elif d['時間3'][2:] in empty_list[int(d['時間3'][0]) - 1] : # 時間3也符合空堂時間
                        if d['教室1'] == 'nan' :
                            d['教室1'] = "" 
                        if d['教室2'] == 'nan' :
                            d['教室2'] = ""
                        if d['教室3'] == 'nan' :
                            d['教室3'] = ""  
                        temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['時間3'], d['教室3'], d['課程代碼'] ] )  
            if temp : # temp有東西 
                result.append( temp.copy() )
    else : # 使用者沒有課表
        for d in classData :
            temp = []
            if d['時間2'] == 'nan' : # 沒時間2
                if d['教室1'] == 'nan' :
                    d['教室1'] = "" 
                temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['課程代碼'] ] )  
            elif d['時間3'] == 'nan' : # 沒時間3
                if d['教室1'] == 'nan' :
                    d['教室1'] = "" 
                if d['教室2'] == 'nan' :
                    d['教室2'] = ""
                temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['課程代碼'] ] )    
            else :
                if d['教室1'] == 'nan' :
                    d['教室1'] = "" 
                if d['教室2'] == 'nan' :
                    d['教室2'] = ""
                if d['教室3'] == 'nan' :
                    d['教室3'] = "" 
                temp.extend( [ d['課程名稱'], d['類別'], d['授課導師'], d['時間1'], d['教室1'], d['時間2'], d['教室2'], d['時間3'], d['教室3'], d['課程代碼'] ] )  
            if temp :
                result.append( temp.copy() )
    if len( result ) > 10 : # 超過10個隨機取10個
        number_of_index = []
        i = 0
        while i < len( result ) :
            number_of_index.append( i )
            i = i + 1
        
        index = random.sample( number_of_index, 10 )
        result_list = []
        for i in index :
            result_list.append( result[ i ] )
        result = result_list
    if result : # result 有東西
        content = make_flex_message.make_course_search_flex(result)
    else :
        content = None
    return content


def Add_Course_Directly( db, id, course_name, course_time, cover ) : # @直接輸入的加入課程方法
    collection = db['class_table']
    class_table = collection.find_one({ '名稱' : id },{ "_id" : 0 })
    # 取出原本的課表
    time_list = []
    for time in course_time : # time為每個1-12-->[ 1, 12 ]
        for t in time[1] : # 將時段分開-->34變成時段3跟時段4
            time_str = "時段" + t
            time_list.append( [ int( time[0] ) - 1, time_str ] )
    if not cover : # 不知道要不要覆蓋
        for course in time_list : # 修改課表-->先看有沒有課
            t = course[1]
            i = course[0]
            if class_table[t][i] != " " : # 有課了 不行!
                return False
    for course in time_list : # 修改課表-->一個改好名字就換上去換完為止唷
        t = course[1]
        i = course[0]
        class_table[t][i] = course_name
        collection.update_one({ '名稱' : id },{ "$set": { t : class_table[t] } })
    return True


def Add_Course( db, id, course_name, course_time, course_day ) : # ADD 之後可能會用到
    collection = db['class_table']
    class_table = collection.find_one({ '名稱' : id },{ "_id" : 0 })
    # 取出原本的課表
    time_list = []
    for time in course_time : # 將時段分開-->34變成時段3跟時段4
        for t in time :
            time_str = "時段" + t
            time_list.append( time_str )

    i = int( course_day )
    for course in time_list : # 修改課表-->一個改好名字就換上去換完為止唷
        class_table[course][i] = course_name
        collection.update_one({ '名稱' : id },{ "$set": { course : class_table[course] } })


def Import_Department_Course( db, id, department ) : # 匯入系所班級
    department_data_collection = db['department_data'] # 查過系所班級會有的東西
    department_data = department_data_collection.find_one({ '班級' : { '$regex': department } },{ "_id" : 0 })
    if department_data != None :
        img_url = department_data['url']
        collection = db['class_table']
        
        new_query = { '班級' : department_data['班級'], '時段A' : department_data['時段A'], 
                '時段1' : department_data['時段1'], '時段2' : department_data['時段2'], 
                '時段3' : department_data['時段3'], '時段4' : department_data['時段4'], 
                '時段B' : department_data['時段B'], '時段5' : department_data['時段5'], 
                '時段6' : department_data['時段6'], '時段7' : department_data['時段7'], 
                '時段8' : department_data['時段8'], '時段C' : department_data['時段C'], 
                '時段D' : department_data['時段D'], '時段E' : department_data['時段E'], 
                '時段F' : department_data['時段F'], '時段G' : department_data['時段G'] }
        collection.update_one({ '名稱' : id },{ "$set": new_query })
        return img_url
    else : # 還沒有資料 直接去生成
        query = "系所班級"
        collection = db['classdata_1111']
        course = collection.find({ '開課班級' : { '$regex': department }, '必選修' : { '$regex': '必' } },{ "_id" : 0 })
        try :
            print( course[0] )
            img_url = convert_to_image.generate_departmentCourseData( db, course ) # 去生成url 順便放資料
            department_data = department_data_collection.find_one({ '班級' : { '$regex': department } },{ "_id" : 0 })
            collection = db['class_table']
            
            new_query = { '班級' : department_data['班級'], '時段A' : department_data['時段A'], 
                    '時段1' : department_data['時段1'], '時段2' : department_data['時段2'], 
                    '時段3' : department_data['時段3'], '時段4' : department_data['時段4'], 
                    '時段B' : department_data['時段B'], '時段5' : department_data['時段5'], 
                    '時段6' : department_data['時段6'], '時段7' : department_data['時段7'], 
                    '時段8' : department_data['時段8'], '時段C' : department_data['時段C'], 
                    '時段D' : department_data['時段D'], '時段E' : department_data['時段E'], 
                    '時段F' : department_data['時段F'], '時段G' : department_data['時段G'] }
            collection.update_one({ '名稱' : id },{ "$set": new_query })
            return img_url
        except :
            return None

    