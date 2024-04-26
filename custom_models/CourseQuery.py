import pymongo

def course_query(db, query, text):
    collection = db['classdata_1101']
    if query == "課程名稱" :
        course = collection.find({ '課程名稱' : { '$regex': text }, '身分' : "大學部" },{ "_id" : 0 })
        try :
            print(course[0])
            return course
        except :
            return None
    elif query == '授課導師' :
        course = collection.find({ '授課導師' : text, '身分' : "大學部" },{ "_id" : 0 })
        try :
            print(course[0])
            return course
        except :
            return None
    elif query == '系所班級' :
        course = collection.find({ '開課班級' : { '$regex': text }, '必選修' : { '$regex': '必' }, '身分' : "大學部" },{ "_id" : 0 })
        try :
            print(course[0])
            return course
        except :
            return None
    elif query == '類別' :
        course = collection.find({ '類別' : text, '身分' : "大學部" },{ "_id" : 0 })
        try :
            print(course[0])
            return course
        except :
            return None
    elif query == '語言' :
        if text[0] == '中' or text[0] == '國' :
            text = '國語'
        elif text[0] == '英' or text[0] == '美' :
            text = '英語'
        elif text[0] == '法' :
            text = '法語'
        elif text[0] == '德' :
            text = '德語'
        elif text[0] == '日' :
            text = '日語'
        elif '西班牙' in text :
            text = '西班牙語'
        elif '印尼' in text :
            text = '印尼語'
        elif text[0] == '韓' :
            text = '韓語'
        elif text[0] == '泰' :
            text = '泰語'
        course = collection.find({ '語言' : text },{ "_id" : 0 })
        try :
            print(course[0])
            return course
        except :
            return None
    elif query == '條件' :
        course = collection.find({ '條件' : { '$regex': text } },{ "_id" : 0 })
        try :
            print(course[0])
            return course
        except :
            return None
        
    
    