from hashlib import new
from pickletools import float8
import time
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import pyimgur
import matplotlib.image as mpimg
from random import choice
import numpy as np
import re
import string
import pymongo
import statistics

plt.rcParams['font.sans-serif'] = ['jf-openhuninn-1.1']#告訴matplotlib設定中文字型

def Recommend_SpecificCourse( userID, token, db ) :
    if token == "No" :
        c = [0.25, 0.25, 0.25, 0.25]
    elif token == "作業量分數" :
        c = [1, 0, 0, 0]
    elif token == "課程難度分數" :
        c = [0, 1, 0, 0]
    elif token == "學到東西分數" :
        c = [0, 0, 1, 0]
    elif token == "給分甜不甜分數" :
        c = [0, 0, 0, 1]
    collection = db['暫存推薦條件']
    collection_com = db['課程評價']
    collection_sort = db['排序']
    temp = collection.find_one({ 'UserID' : userID })
    class_name = temp['課程名稱']
    teacher_name = temp['老師名稱']
    comment = collection_com.find_one({ '課程名稱' : class_name, '老師名稱' : teacher_name })
    s1 = []
    s2 = []
    s3 = []
    s4 = []
    for i in range( len( comment['UserID'] ) ) :
        s1.append( comment['作業量分數'][i] )
        s2.append( comment['課程難度分數'][i] )
        s3.append( comment['學到東西分數'][i] )
        s4.append( comment['給分甜不甜分數'][i] )
    if len( s1 ) >= 100 :
        #要做資料可信度的東東哦
        for i in range( len( s1 ) ) :
            s1[i] = s1[i]*10
            s2[i] = s2[i]*10
            s3[i] = s3[i]*10
            s4[i] = s4[i]*10
        v = []
        v.append( s1 )
        v.append( s2 )
        v.append( s3 )
        v.append( s4 )
        for i in range( 4 ) :
            mean = sum(v[i])/len(v[i])
            dev = statistics.pstdev(v[i])
            v[i] = np.minimum( v[i], mean+dev )
            v[i] = np.maximum( v[i], mean-dev )
        s1 = v[0]
        s2 = v[1]
        s3 = v[2]
        s4 = v[3]
    for i in range( len( s1 ) ) :
        sorted = collection_sort.find_one({ 'UserID' : userID, '課程名稱' : comment['課程名稱'], '老師名稱' : comment['老師名稱'], '課程代碼' : comment['課程代碼'] })
        if sorted != None :
            score = ( float(s1[i])*float(c[0]) + float(s2[i])*float(c[1]) + float(s3[i])*float(c[2]) + float(s4[i])*float(c[3]) )*100/5
            sorted['個數'] = str( int( sorted['個數'] ) + 1 )
            sorted['加權分數'] = str( float( sorted['加權分數'] ) + score )
            collection_sort.update_one({ 'UserID' : userID, '課程名稱' : sorted['課程名稱'], '課程代碼' : sorted['課程代碼'] },{ "$set" : { '加權分數' : sorted['加權分數'], '個數' : sorted['個數'] } })
        else :
            score = str(( float(s1[i])*float(c[0]) + float(s2[i])*float(c[1]) + float(s3[i])*float(c[2]) + float(s4[i])*float(c[3]) )*100/5 )
            query = { 'UserID' : userID, '課程名稱' : comment['課程名稱'], '老師名稱' : comment['老師名稱'], '課程代碼' : comment['課程代碼'], '加權分數' : score, '個數' : "1" }
            collection_sort.insert_one( query )
    calculate = collection_sort.find( { "UserID" : userID } )
    for s in calculate :
        s['加權分數'] = str( float( s['加權分數'] ) / int( s['個數'] ) )
        collection_sort.update_one( { 'UserID' : userID, '課程名稱' : s['課程名稱'] }, { "$set" : { '加權分數' : s['加權分數'] } } )
    return collection_sort.find_one({ "UserID" : userID })

def Recommend_GeneralEducation( userID, token, db ) :
    if token == "No" :
        c = [0.25, 0.25, 0.25, 0.25]
    elif token == "作業量分數" :
        c = [1, 0, 0, 0]
    elif token == "課程難度分數" :
        c = [0, 1, 0, 0]
    elif token == "學到東西分數" :
        c = [0, 0, 1, 0]
    elif token == "給分甜不甜分數" :
        c = [0, 0, 0, 1]
    collection = db['暫存推薦條件']
    collection_com = db['課程評價']
    collection_sort = db['排序']
    temp = collection.find_one({ 'UserID' : userID })
    tp = temp['類別']
    comment = collection_com.find({ '課程類別' : tp })
    if comment != None :
        for m in comment :
            s1 = []
            s2 = []
            s3 = []
            s4 = []
            for i in range( len( m['UserID'] ) ) :
                s1.append( m['作業量分數'][i] )
                s2.append( m['課程難度分數'][i] )
                s3.append( m['學到東西分數'][i] )
                s4.append( m['給分甜不甜分數'][i] )
                if len( s1 ) >= 100 :
                    #要做資料可信度的東東哦
                    for i in range( len( s1 ) ) :
                        s1[i] = s1[i]*10
                        s2[i] = s2[i]*10
                        s3[i] = s3[i]*10
                        s4[i] = s4[i]*10
                    v = []
                    v.append( s1 )
                    v.append( s2 )
                    v.append( s3 )
                    v.append( s4 )
                    for i in range( 4 ) :
                        mean = sum(v[i])/len(v[i])
                        dev = statistics.pstdev(v[i])
                        v[i] = np.minimum( v[i], mean+dev )
                        v[i] = np.maximum( v[i], mean-dev )
                    s1 = v[0]
                    s2 = v[1]
                    s3 = v[2]
                    s4 = v[3]
            sorted = collection_sort.find_one({ 'UserID' : userID, '課程名稱' : m['課程名稱'], '老師名稱' : m['老師名稱'], '課程代碼' : m['課程代碼'] })
            if sorted != None :
                for i in range( len( s1 ) ) :
                    score = ( float(s1[i])*float(c[0]) + float(s2[i])*float(c[1]) + float(s3[i])*float(c[2]) + float(s4[i])*float(c[3]) )*100/5
                    sorted['個數'] = str( int( sorted['個數'] ) + 1 )
                    sorted['加權分數'] = str( float( sorted['加權分數'] ) + score )
                    collection_sort.update_one({ 'UserID' : userID, '課程名稱' : m['課程名稱'], '老師名稱' : m['老師名稱'], '課程代碼' : m['課程代碼'] },{ "$set" : { '加權分數' : sorted['加權分數'], '個數' : sorted['個數'] } })
            else :
                for i in range( len( s1 ) ) :
                    score = str(( float(s1[i])*float(c[0]) + float(s2[i])*float(c[1]) + float(s3[i])*float(c[2]) + float(s4[i])*float(c[3]) )*100/5 )
                    query = { 'UserID' : userID, '課程名稱' : m['課程名稱'], '老師名稱' : m['老師名稱'], '課程代碼' : m['課程代碼'], '加權分數' : score, '個數' : "1" }
                    collection_sort.insert_one( query )
            i = i + 1
    case = 1
    return makeTop10List( userID, db, case )       

def Recommend_DepartmentCourse( userID, token, db ) :
    if token == "No" :
        c = [0.25, 0.25, 0.25, 0.25]
    elif token == "作業量分數" :
        c = [1, 0, 0, 0]
    elif token == "課程難度分數" :
        c = [0, 1, 0, 0]
    elif token == "學到東西分數" :
        c = [0, 0, 1, 0]
    elif token == "給分甜不甜分數" :
        c = [0, 0, 0, 1]
    collection = db['暫存推薦條件']
    collection_data = db['classdata_1111']
    collection_com = db['課程評價']
    collection_sort = db['排序']
    temp = collection.find_one({ 'UserID' : userID })
    dept = temp['系級']
    course = collection_data.find({ '開課班級' : { '$regex': dept }, '必選修' : { '$regex': '選' } }) #course為所有此開課班級的選修課
    course_list = []
    for s in course :
        if '碩' in s['開課班級'] or '博' in s['開課班級'] :
            pass
        else :
            course_list.append( s )
    comment = collection_com.find() #comment為評論中符合目前課程名稱的評論
    if comment != None :
        comment_list = []
        for s in comment :
            comment_list.append( s )
        for s in course_list :
            for m in range( len( comment_list ) ) :
                if comment_list[m]['課程代碼'] == s['課程代碼'] and comment_list[m]['老師名稱'] == s['授課導師'] :
                    s1 = []
                    s2 = []
                    s3 = []
                    s4 = []
                    for i in range( len( comment_list[m]['UserID'] ) ) :
                        s1.append( comment_list[m]['作業量分數'][i] )
                        s2.append( comment_list[m]['課程難度分數'][i] )
                        s3.append( comment_list[m]['學到東西分數'][i] )
                        s4.append( comment_list[m]['給分甜不甜分數'][i] )
                        if len( s1 ) >= 100 :
                            #要做資料可信度的東東哦
                            for i in range( len( s1 ) ) :
                                s1[i] = s1[i]*10
                                s2[i] = s2[i]*10
                                s3[i] = s3[i]*10
                                s4[i] = s4[i]*10
                            v = []
                            v.append( s1 )
                            v.append( s2 )
                            v.append( s3 )
                            v.append( s4 )
                            for i in range( 4 ) :
                                mean = sum(v[i])/len(v[i])
                                dev = statistics.pstdev(v[i])
                                v[i] = np.minimum( v[i], mean+dev )
                                v[i] = np.maximum( v[i], mean-dev )
                            s1 = v[0]
                            s2 = v[1]
                            s3 = v[2]
                            s4 = v[3]

                    sorted = collection_sort.find_one({ 'UserID' : userID, '課程名稱' : s['課程名稱'], '老師名稱' : s['授課導師'], '課程代碼' : s['課程代碼'] })
                    if sorted != None :
                        for i in range( len( s1 ) ) :
                            score = ( float(s1[i])*float(c[0]) + float(s2[i])*float(c[1]) + float(s3[i])*float(c[2]) + float(s4[i])*float(c[3]) )*100/5
                        if score != 0 :
                            sorted['個數'] = str( int( sorted['個數'] ) + 1 )
                            sorted['加權分數'] = str( float( sorted['加權分數'] ) + score )
                            collection_sort.update_one({ 'UserID' : userID, '課程名稱' : s['課程名稱'], '課程代碼' : s['課程代碼'] },{ "$set" : { '加權分數' : sorted['加權分數'], '個數' : sorted['個數'] } })
                    else :
                        for i in range( len( s1 ) ) :
                            score = str(( float(s1[i])*float(c[0]) + float(s2[i])*float(c[1]) + float(s3[i])*float(c[2]) + float(s4[i])*float(c[3]) )*100/5 )
                        if int(float(score)) != 0 :
                            query = { 'UserID' : userID, '課程名稱' : s['課程名稱'], '老師名稱' : s['授課導師'], '課程代碼' : s['課程代碼'], '加權分數' : score, '個數' : "1" }
                            collection_sort.insert_one( query )
    case = 1
    return makeTop10List( userID, db, case )

def makeTop10List( userID, db, case ) :
    collection_sort = db['排序']
    collection_unUsed = db['下一批']
    top10 = []
    to_sort = []
    if case == 1 :
        temp = collection_sort.find({ 'UserID' : userID })
        for s in temp :
            query = { '課程名稱' : s['課程名稱'], '老師名稱' : s['老師名稱'], '課程代碼' : s['課程代碼'], '加權分數' : s['加權分數'], '個數' : s['個數'] }
            to_sort.append( query )
        for s in to_sort :
            s['加權分數'] = float( s['加權分數'] )/int( s['個數'] )
            if len(top10) < 10 :
                top10.append( s )
            elif len(top10) == 10 :
                smallest = -1
                for i in range(10) :
                    if s['加權分數'] > top10[i]['加權分數'] :
                        if smallest == -1 :
                            smallest = i
                        else :
                            if top10[smallest]['加權分數'] > top10[i]['加權分數'] :
                                smallest = i
                if smallest != -1 :
                    query = { 'UserID' : userID, 'case' : 1, '課程名稱' : top10[smallest]['課程名稱'], '老師名稱' : top10[smallest]['老師名稱'], '課程代碼' : top10[smallest]['課程代碼'], '加權分數' : top10[smallest]['加權分數'] }
                    top10[smallest] = s
                else :
                    query = { 'UserID' : userID, 'case' : 1, '課程名稱' : s['課程名稱'], '老師名稱' : s['老師名稱'],'課程代碼':s['課程代碼'], '加權分數' : s['加權分數'] }
                collection_unUsed.insert_one(query)
        for i in range(len(top10)-1) :
            for u in range(i+1,len(top10)) :
                if top10[i]['加權分數'] < top10[u]['加權分數'] :
                    temp = top10[i]
                    top10[i] = top10[u]
                    top10[u] = temp
        if len(top10) != 0 :
            return top10
        else :
            return None
    elif case == 2 :
        collection_sort.delete_many({ "UserID" : userID })
        tempList = collection_unUsed.find({ "UserID" : userID })
        nextList = []
        for s in tempList :
            nextList.append( s )
        if len(nextList) == 1 :
            toReturn = []
            toReturn.append( nextList[0] )
            collection_unUsed.delete_one({ 'UserID' : userID, 'case' : 1, '課程名稱' : s['課程名稱'], '老師名稱' : s['老師名稱'], '課程代碼' : s['課程代碼'], '加權分數' : s['加權分數'] })
            return toReturn
        else :
            for s in nextList :
                if len(top10) < 10 :
                    top10.append( s )
                elif len(top10) == 10 :
                    smallest = -1
                    for i in range(10) :
                        if s['加權分數'] > top10[i]['加權分數'] :
                            if smallest == -1 :
                                smallest = i
                            else :
                                if top10[smallest]['加權分數'] > top10[i]['加權分數'] :
                                    smallest = i
                    if smallest != -1 :
                        top10[smallest] = s
            for i in range(len(top10)-1) :
                for u in range(i+1,len(top10)) :
                    if top10[u]['加權分數'] > top10[i]['加權分數'] :
                        temp = top10[i]
                        top10[i] = top10[u]
                        top10[u] = temp
            for s in top10 :
                collection_unUsed.delete_one({ 'UserID' : userID, '課程名稱' : s['課程名稱'], '老師名稱' : s['老師名稱'], '課程代碼' : s['課程代碼'], '加權分數' : s['加權分數'] })
        return top10
                

        

# def made_pic( top10 ) :
#     table_top10 = pd.DataFrame( top10 )
#     fig, ax = plt.subplots()
#     height = np.array(table_top10['加權分數'].tolist(), dtype="float64")
#     a = []
#     for i in range(len(table_top10['課程名稱'])) :
#         a.append(i+1)
#     left = np.array(a)
#     labels = table_top10['課程名稱']
#     ax.bar( left, height, alpha=0.5, width=0.2, color='pink', ec='blue', tick_label = labels )
#     title = "\n以下為推薦結果"
#     ax.set_title(label = title)
#     ax.set(xlim=(0,11), xticks=np.arange(1,11), ylim=(0,100))
#     ax.set_xlabel('課程名稱\n')
#     ax.set_ylabel('\n好評百分比(%)')
#     plt.xticks(fontsize=10, rotation=-30)
#     plt.show()
#     fig.savefig("new.png",bbox_inches='tight',pad_inches = 0)
#     CLIENT_ID = "d98ba63f9e15ae8" # 舊ID
#     time.sleep(0.1)
#     PATH = "new.png"
#     im = pyimgur.Imgur(CLIENT_ID)
#     uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
#     plt.clf()
#     return uploaded_image.link 