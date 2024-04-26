import pymongo
from random import sample

def outputTextComment( db, userID, courseName, courseId ) :
    collection = db['課程評價']
    returnList = []
    courseList = collection.find_one({ "課程名稱" : courseName, "課程代碼" : courseId })
    if courseList != None:
        i = 0
        for s in courseList['文字評論'] :
            if len( s ) != 0 :
                query = { "UserID" : userID, "case" : 2, "老師名稱" : courseList['老師名稱'], "課程代碼" : courseId, "文字評論" : s }
                returnList.append( query )
        if len( returnList ) > 10 :
            collection_unUsed = db['下一批']
            newList = sample( returnList, len(returnList) )
            for i in range( 10, len(newList) ) :
                query = { "UserID" : userID, "case" : 2, "課程名稱" : courseName, "老師名稱" : newList[i]['老師名稱'], "課程代碼" : newList[i]['課程代碼'], "文字評論" : newList[i]['文字評論'] }
                collection_unUsed.insert_one( query )
            return newList
        elif len( returnList ) <= 10 and len( returnList ) > 0 :
            return returnList
        else :
            return None
    else:
        return None
def returnUnused( db, userID ) :
    collection = db['下一批']
    toReturnList = []
    temp = collection.find({ 'UserID' : userID })
    for s in temp :
        toReturnList.append( s )
        collection.delete_one({ 'UserID' : userID, 'case' : 2, '課程名稱' : s['課程名稱'], '老師名稱' : s['老師名稱'], '課程代碼' : s['課程代碼'], '文字評論' : s['文字評論'] })
    return toReturnList