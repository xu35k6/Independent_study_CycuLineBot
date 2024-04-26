import time
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import pyimgur
import pymongo
import matplotlib.image as mpimg
from random import choice
from custom_models import set_color
plt.rcParams['font.sans-serif'] = ['jf-openhuninn-1.1']#告訴matplotlib設定中文字型
    
def generate_courseData(db, coursedata, keyword) : # 體育課程
    # DataFrame=>png
    plt.rcParams['font.size'] = 14 #字體大小
    plt.rcParams['savefig.dpi'] = 200 #图片像素
    plt.rcParams['figure.figsize'] = (5.0, 3.0) # 圖片大小
    courses = []
    change = True # 需不需要改圖大小
    for list in coursedata :
        data = []
        data.append(list['課程代碼'])
        data.append(list['課程名稱'])
        data.append(list['授課導師'])
        data.append(list['時間1'])
        if list['條件'] == 'nan' :
            data.append('無')
        else :
            data.append(list['條件'])
            if len(list['條件']) > 13 : # 備註太長 字會太小
                change = False
                plt.rcParams['figure.figsize'] = (15.0, 2.0) # 圖片大小
            elif len(list['條件']) > 8 : # 備註太長 字會太小
                change = False
                plt.rcParams['figure.figsize'] = (6.0, 3.0) # 圖片大小
        courses.append(data)
    # 用Pandas將樣本轉成DataFrame
    table_pd = pd.DataFrame(courses)
    table_pd.columns=['課程代碼', '課程名稱', '授課導師', '時間', '備註']
    i = 1
    index = []
    while i <= len(courses) : # 不確定找到幾個 一個一個加 最多10個
        if i == 1 :
            index.append('1')
        elif i == 2 :
            index.append('2')
        elif i == 3 :
            index.append('3')
        elif i == 4 :
            index.append('4')
        elif i == 5 :
            index.append('5')
            if change :
                plt.rcParams['figure.figsize'] = (7.0, 3.0) # 圖片大小 超過就用大一點
        elif i == 6 :
            index.append('6')
        elif i == 7 :
            index.append('7')
        elif i == 8 :
            index.append('8')
        elif i == 9 :
            index.append('9')
        elif i == 10 :
            index.append('10')
            if change :
                plt.rcParams['figure.figsize'] = (5.0, 3.0) # 圖片大小 超過就用大一點
        i = i + 1
    table_pd.index=index
    plt.figure('123')            # 視窗名稱
    ax = plt.axes(frame_on=False)# 不要額外框線
    title = "\n" + "keyword : " + keyword
    ax.table = set_color.set_color_sport(courses, table_pd, title)
    pd.plotting.table(ax, table_pd, loc='center') #將mytable投射到ax上，且放置於ax的中間

    collection_qrcode = db['mimo_qrcode'] # 抓浮水印圖~
    mimo_img = []
    for item in collection_qrcode.find() :
        mimo_img.append( item )
    choose_img = choice(mimo_img) # 選一個浮水印
    PATH = choose_img['url'] # 浮水印的網址唷
    
    qrcode = mpimg.imread(PATH)
    qrcode.shape
    if choose_img['名稱'] != "qrcode" : # 不是普通版的 大小要調整
        axe_base = plt.axes([0.55, 0.72, 0.53, 0.53], frame_on=False) # 位置 大小
    else :
        axe_base = plt.axes([0.7, 0.8, 0.2, 0.2], frame_on=False)
    axe_base.xaxis.set_visible(False)  # 隱藏X軸刻度線
    axe_base.yaxis.set_visible(False)  # 隱藏Y軸刻度線
    plt.imshow(qrcode)
    
    plt.savefig("send.png",bbox_inches='tight',pad_inches = 0)
    CLIENT_ID = "imgur的ID" # 舊ID
    PATH = "send.png"
    time.sleep(0.1)
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    print(table_pd)
    plt.clf()
    return uploaded_image.link

def generate_departmentCourseData(db, course) : #系所班級
    collection = db['department_data']
    plt.rcParams['font.size'] = 14 #字體大小
    plt.rcParams['savefig.dpi'] = 250 #图片像素
    plt.rcParams['figure.figsize'] = (5.0, 4.0) # 圖片大小
    data = []
    time_a = [ " ", " ", " ", " ", " ", " ", " " ] # 先初始化
    time_1 = [ " ", " ", " ", " ", " ", " ", " " ]
    time_2 = [ " ", " ", " ", " ", " ", " ", " " ]
    time_3 = [ " ", " ", " ", " ", " ", " ", " " ]
    time_4 = [ " ", " ", " ", " ", " ", " ", " " ]
    time_b = [ " ", " ", " ", " ", " ", " ", " " ]
    time_5 = [ " ", " ", " ", " ", " ", " ", " " ]
    time_6 = [ " ", " ", " ", " ", " ", " ", " " ]
    time_7 = [ " ", " ", " ", " ", " ", " ", " " ]
    time_8 = [ " ", " ", " ", " ", " ", " ", " " ]
    time_c = [ " ", " ", " ", " ", " ", " ", " " ]
    time_d = [ " ", " ", " ", " ", " ", " ", " " ]
    time_e = [ " ", " ", " ", " ", " ", " ", " " ]
    time_f = [ " ", " ", " ", " ", " ", " ", " " ]
    time_g = [ " ", " ", " ", " ", " ", " ", " " ]
    class_name = ""
    for item in course :
        class_time = item['時間1']
        class_name = item['開課班級']
        try :
            day = int(class_time[0]) - 1
            num = len(class_time) - 2
            room = item['教室1']
            if room == 'nan' :
                room = ' '
            name = item['課程名稱']
            if class_time[2] == 'A' :
                time_a[day] = name + "\n" + room
                if num >= 2 :
                    time_1[day] = name + "\n" + room
                    if num == 3 :
                        time_2[day] = name + "\n" + room
            elif class_time[2] == '1' :
                time_1[day] = name + "\n" + room
                if num >= 2 :
                    time_2[day] = name + "\n" + room
                    if num == 3 :
                        time_3[day] = name + "\n" + room
            elif class_time[2] == '2' :
                time_2[day] = name + "\n" + room
                if num >= 2 :
                    time_3[day] = name + "\n" + room
                    if num == 3 :
                        time_4[day] = name + "\n" + room
            elif class_time[2] == '3' :
                time_3[day] = name + "\n" + room
                if num >= 2 :
                    time_4[day] = name + "\n" + room
                    if num == 3 :
                        time_b[day] = name + "\n" + room
            elif class_time[2] == '4' :
                time_4[day] = name + "\n" + room
                if num >= 2 :
                    time_b[day] = name + "\n" + room
                    if num == 3 :
                        time_5[day] = name + "\n" + room
            elif class_time[2] == 'b' :
                time_b[day] = name + "\n" + room
                if num >= 2 :
                    time_5[day] = name + "\n" + room
                    if num == 3 :
                        time_6[day] = name + "\n" + room
            elif class_time[2] == '5' :
                time_5[day] = name + "\n" + room
                if num >= 2 :
                    time_6[day] = name + "\n" + room
                    if num == 3 :
                        time_7[day] = name + "\n" + room
            elif class_time[2] == '6' :
                time_6[day] = name + "\n" + room
                if num >= 2 :
                    time_7[day] = name + "\n" + room
                    if num == 3 :
                        time_8[day] = name + "\n" + room
            elif class_time[2] == '7' :
                time_7[day] = name + "\n" + room
                if num >= 2 :
                    time_8[day] = name + "\n" + room
                    if num == 3 :
                        time_c[day] = name + "\n" + room
            elif class_time[2] == '8' :
                time_8[day] = name + "\n" + room
                if num >= 2 :
                    time_c[day] = name + "\n" + room
                    if num == 3 :
                        time_d[day] = name + "\n" + room
            elif class_time[2] == 'c' :
                time_c[day] = name + "\n" + room
                if num >= 2 :
                    time_d[day] = name + "\n" + room
                    if num == 3 :
                        time_e[day] = name + "\n" + room
            elif class_time[2] == 'd' :
                time_d[day] = name + "\n" + room
                if num >= 2 :
                    time_e[day] = name + "\n" + room
                    if num == 3 :
                        time_f[day] = name + "\n" + room
            elif class_time[2] == 'e' :
                time_e[day] = name + "\n" + room
                if num >= 2 :
                    time_f[day] = name + "\n" + room
                    if num == 3 :
                        time_g[day] = name + "\n" + room
            elif class_time[2] == 'f' :
                time_f[day] = name + "\n" + room
                if num >= 2 :
                    time_g[day] = name + "\n" + room
            elif class_time[2] == 'g' :
                time_g[day] = name + "\n" + room

            class_time = item['時間2']
            day = int(class_time[0]) - 1
            num = len(class_time) - 2
            room = item['教室2']
            if room == 'nan' :
                room = ' '
            if class_time != 'nan' :
                if class_time[2] == 'A' :
                    time_a[day] = name + "\n" + room
                    if num >= 2 :
                        time_1[day] = name + "\n" + room
                        if num == 3 :
                            time_2[day] = name + "\n" + room
                elif class_time[2] == '1' :
                    time_1[day] = name + "\n" + room
                    if num >= 2 :
                        time_2[day] = name + "\n" + room
                        if num == 3 :
                            time_3[day] = name + "\n" + room
                elif class_time[2] == '2' :
                    time_2[day] = name + "\n" + room
                    if num >= 2 :
                        time_3[day] = name + "\n" + room
                        if num == 3 :
                            time_4[day] = name + "\n" + room
                elif class_time[2] == '3' :
                    time_3[day] = name + "\n" + room
                    if num >= 2 :
                        time_4[day] = name + "\n" + room
                        if num == 3 :
                            time_b[day] = name + "\n" + room
                elif class_time[2] == '4' :
                    time_4[day] = name + "\n" + room
                    if num >= 2 :
                        time_b[day] = name + "\n" + room
                        if num == 3 :
                            time_5[day] = name + "\n" + room
                elif class_time[2] == 'b' :
                    time_b[day] = name + "\n" + room
                    if num >= 2 :
                        time_5[day] = name + "\n" + room
                        if num == 3 :
                            time_6[day] = name + "\n" + room
                elif class_time[2] == '5' :
                    time_5[day] = name + "\n" + room
                    if num >= 2 :
                        time_6[day] = name + "\n" + room
                        if num == 3 :
                            time_7[day] = name + "\n" + room
                elif class_time[2] == '6' :
                    time_6[day] = name + "\n" + room
                    if num >= 2 :
                        time_7[day] = name + "\n" + room
                        if num == 3 :
                            time_8[day] = name + "\n" + room
                elif class_time[2] == '7' :
                    time_7[day] = name + "\n" + room
                    if num >= 2 :
                        time_8[day] = name + "\n" + room
                        if num == 3 :
                            time_c[day] = name + "\n" + room
                elif class_time[2] == '8' :
                    time_8[day] = name + "\n" + room
                    if num >= 2 :
                        time_c[day] = name + "\n" + room
                        if num == 3 :
                            time_d[day] = name + "\n" + room
                elif class_time[2] == 'c' :
                    time_c[day] = name + "\n" + room
                    if num >= 2 :
                        time_d[day] = name + "\n" + room
                        if num == 3 :
                            time_e[day] = name + "\n" + room
                elif class_time[2] == 'd' :
                    time_d[day] = name + "\n" + room
                    if num >= 2 :
                        time_e[day] = name + "\n" + room
                        if num == 3 :
                            time_f[day] = name + "\n" + room
                elif class_time[2] == 'e' :
                    time_e[day] = name + "\n" + room
                    if num >= 2 :
                        time_f[day] = name + "\n" + room
                        if num == 3 :
                            time_g[day] = name + "\n" + room
                elif class_time[2] == 'f' :
                    time_f[day] = name + "\n" + room
                    if num >= 2 :
                        time_g[day] = name + "\n" + room
                elif class_time[2] == 'g' :
                    time_g[day] = name + "\n" + room

            
            class_time = item['時間3']
            day = int(class_time[0]) - 1
            num = len(class_time) - 2
            room = item['教室3']
            if room == 'nan' :
                room = ' '
            if class_time != 'nan' :
                if class_time[2] == 'A' :
                    time_a[day] = name + "\n" + room
                    if num >= 2 :
                        time_1[day] = name + "\n" + room
                        if num == 3 :
                            time_2[day] = name + "\n" + room
                elif class_time[2] == '1' :
                    time_1[day] = name + "\n" + room
                    if num >= 2 :
                        time_2[day] = name + "\n" + room
                        if num == 3 :
                            time_3[day] = name + "\n" + room
                elif class_time[2] == '2' :
                    time_2[day] = name + "\n" + room
                    if num >= 2 :
                        time_3[day] = name + "\n" + room
                        if num == 3 :
                            time_4[day] = name + "\n" + room
                elif class_time[2] == '3' :
                    time_3[day] = name + "\n" + room
                    if num >= 2 :
                        time_4[day] = name + "\n" + room
                        if num == 3 :
                            time_b[day] = name + "\n" + room
                elif class_time[2] == '4' :
                    time_4[day] = name + "\n" + room
                    if num >= 2 :
                        time_b[day] = name + "\n" + room
                        if num == 3 :
                            time_5[day] = name + "\n" + room
                elif class_time[2] == 'b' :
                    time_b[day] = name + "\n" + room
                    if num >= 2 :
                        time_5[day] = name + "\n" + room
                        if num == 3 :
                            time_6[day] = name + "\n" + room
                elif class_time[2] == '5' :
                    time_5[day] = name + "\n" + room
                    if num >= 2 :
                        time_6[day] = name + "\n" + room
                        if num == 3 :
                            time_7[day] = name + "\n" + room
                elif class_time[2] == '6' :
                    time_6[day] = name + "\n" + room
                    if num >= 2 :
                        time_7[day] = name + "\n" + room
                        if num == 3 :
                            time_8[day] = name + "\n" + room
                elif class_time[2] == '7' :
                    time_7[day] = name + "\n" + room
                    if num >= 2 :
                        time_8[day] = name + "\n" + room
                        if num == 3 :
                            time_c[day] = name + "\n" + room
                elif class_time[2] == '8' :
                    time_8[day] = name + "\n" + room
                    if num >= 2 :
                        time_c[day] = name + "\n" + room
                        if num == 3 :
                            time_d[day] = name + "\n" + room
                elif class_time[2] == 'c' :
                    time_c[day] = name + "\n" + room
                    if num >= 2 :
                        time_d[day] = name + "\n" + room
                        if num == 3 :
                            time_e[day] = name + "\n" + room
                elif class_time[2] == 'd' :
                    time_d[day] = name + "\n" + room
                    if num >= 2 :
                        time_e[day] = name + "\n" + room
                        if num == 3 :
                            time_f[day] = name + "\n" + room
                elif class_time[2] == 'e' :
                    time_e[day] = name + "\n" + room
                    if num >= 2 :
                        time_f[day] = name + "\n" + room
                        if num == 3 :
                            time_g[day] = name + "\n" + room
                elif class_time[2] == 'f' :
                    time_f[day] = name + "\n" + room
                    if num >= 2 :
                        time_g[day] = name + "\n" + room
                elif class_time[2] == 'g' :
                    time_g[day] = name + "\n" + room
        except :
            error = True

    data.append(time_a)
    data.append(time_1)
    data.append(time_2)
    data.append(time_3)
    data.append(time_4)
    data.append(time_b)
    data.append(time_5)
    data.append(time_6)
    data.append(time_7)
    data.append(time_8)
    data.append(time_c)
    data.append(time_d)
    data.append(time_e)
    data.append(time_f)
    data.append(time_g)
    table_pd = pd.DataFrame(data)
    table_pd.columns=['週一', '週二', '週三', '週四', '週五', '週六', '週日' ]
    table_pd.index=['A', '1', '2', '3', '4', 'B', '5', '6', '7', '8', 'C', 'D', 'E', 'F', 'G']
    plt.figure('class')            # 視窗名稱
    ax = plt.axes(frame_on=False)# 不要額外框線
    title = "\n" + class_name + "的課表"
    ax.table = set_color.set_color(data, table_pd, title)
    pd.plotting.table(ax, table_pd, loc='center') #將mytable投射到ax上，且放置於ax的中間
    
    # collection_qrcode = db['mimo_qrcode'] # 抓浮水印圖~
    # mimo_img = []
    # for item in collection_qrcode.find() :
    #     mimo_img.append( item )
    # choose_img = choice(mimo_img) # 選一個浮水印
    # PATH = choose_img['url'] # 浮水印的網址唷
    
    # qrcode = mpimg.imread(PATH)
    # qrcode.shape
    # if choose_img['名稱'] != "qrcode" : # 不是普通版的 大小要調整
    #     axe_base = plt.axes([0.63, 0.72, 0.4, 0.4], frame_on=False) # 位置 大小
    # else :
    #     axe_base = plt.axes([0.75, 0.85, 0.13, 0.13], frame_on=False )
    # axe_base.xaxis.set_visible(False)  # 隱藏X軸刻度線
    # axe_base.yaxis.set_visible(False)  # 隱藏Y軸刻度線
    # plt.imshow(qrcode)

    plt.savefig("class.png",bbox_inches='tight',pad_inches = 0)
    CLIENT_ID = "d98ba63f9e15ae8" # 舊ID
    time.sleep(0.1)
    PATH = "class.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    plt.clf()
    class_data = { '班級' : class_name, 'url' : uploaded_image.link, '時段A' : time_a, '時段1' : time_1, '時段2' : time_2, '時段3' : time_3, '時段4' : time_4, '時段B' : time_b, '時段5' : time_5, '時段6' : time_6,
                '時段7' : time_7, '時段8' : time_8, '時段C' : time_c, '時段D' : time_d, '時段E' : time_e, '時段F' : time_f, '時段G' : time_g }
    collection.insert_one( class_data )
    return uploaded_image.link
 
def Generate_new_table( db, course ) : # 完成課表
    plt.rcParams['font.size'] = 14 #字體大小
    plt.rcParams['savefig.dpi'] = 250 #图片像素
    plt.rcParams['figure.figsize'] = (5.0, 4.0) # 圖片大小
    data = []
    data.append( course['時段A'] )
    data.append( course['時段1'] )  
    data.append( course['時段2'] )  
    data.append( course['時段3'] )  
    data.append( course['時段4'] )  
    data.append( course['時段B'] )  
    data.append( course['時段5'] )  
    data.append( course['時段6'] )  
    data.append( course['時段7'] )  
    data.append( course['時段8'] )  
    data.append( course['時段C'] )  
    data.append( course['時段D'] )  
    data.append( course['時段E'] )  
    data.append( course['時段F'] )  
    data.append( course['時段G'] )  
    table_pd = pd.DataFrame(data)
    
    table_pd.columns=['週一', '週二', '週三', '週四', '週五', '週六', '週日' ]
    table_pd.index=['A', '1', '2', '3', '4', 'B', '5', '6', '7', '8', 'C', 'D', 'E', 'F', 'G']
    plt.figure('new') 
    ax = plt.axes(frame_on=False)# 不要額外框線
    title = "\n您的課表"
    ax.table = set_color.set_color(data, table_pd, title)
    pd.plotting.table(ax, table_pd, loc='center', colLabels=table_pd.columns, rowLabels=table_pd.index ) #將mytable投射到ax上，且放置於ax的中間
    # print("1")
    # collection_qrcode = db['mimo_qrcode'] # 抓浮水印圖~
    # print("2")
    # mimo_img = []
    # for item in collection_qrcode.find() :
    #     mimo_img.append( item )
    # choose_img = choice(mimo_img) # 選一個浮水印
    # PATH = choose_img['url'] # 浮水印的網址唷
    
    # qrcode = mpimg.imread(PATH)
    # qrcode.shape
    # if choose_img['名稱'] != "qrcode" : # 不是普通版的 大小要調整
    #     axe_base = plt.axes([0.63, 0.72, 0.4, 0.4], frame_on=False) # 位置 大小
    # else :
    #     axe_base = plt.axes([0.75, 0.85, 0.13, 0.13], frame_on=False )
    # axe_base.xaxis.set_visible(False)  # 隱藏X軸刻度線
    # axe_base.yaxis.set_visible(False)  # 隱藏Y軸刻度線
    # plt.imshow(qrcode)

    plt.savefig("new.png",bbox_inches='tight',pad_inches = 0)
    CLIENT_ID = "d98ba63f9e15ae8" # 舊ID
    time.sleep(0.1)
    PATH = "new.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    plt.clf()
    return uploaded_image.link

#列出目前有的字體
'''import matplotlib.font_manager
 
a = sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])
 
for i in a:
    print(i)'''