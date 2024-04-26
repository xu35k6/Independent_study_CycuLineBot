from hashlib import new
from pickletools import float8
import time
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import pyimgur
import pymongo
import matplotlib.image as mpimg
from random import choice
import numpy as np
import re
import string
import pymongo
plt.rcParams['font.sans-serif'] = ['jf-openhuninn-1.1']#告訴matplotlib設定中文字型

def MakeList( db, id ) :
    plt.rcParams['font.size'] = 14 #字體大小
    plt.rcParams['savefig.dpi'] = 250 #图片像素
    plt.rcParams['figure.figsize'] = (8.0, 6.0) # 圖片大小
    collection = db['存已修課程']
    list = collection.find_one({ 'UserID' : id })
    Tname = []
    i = 0
    for s in list['課程代碼'] :
        name =  "classdata_" + list['課程年分'][i]
        fcollection = db[name]
        temp = fcollection.find_one({ '課程代碼' : s })
        Tname.append( temp['授課導師'] )
        i = i + 1
    print("結束")
    query = { '課程年分' : list['課程年分'], '課程代碼' : list['課程代碼'], '課程名稱' : list['課程名稱'], '老師名稱' : Tname , '學分' : list['學分'], '分數' : list['分數'] }
    table_pd = pd.DataFrame( query )
    plt.figure('new')
    ax = plt.axes(frame_on=False)# 不要額外框線
    ax.axis('tight')
    ax.axis('off')
    pd.plotting.table(ax, table_pd, loc='center', colLabels=table_pd.columns, rowLabels=table_pd.index )
    plt.savefig("new.png",bbox_inches='tight',pad_inches = 0)
    CLIENT_ID = "d98ba63f9e15ae8" # 舊ID
    time.sleep(0.1)
    PATH = "new.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    plt.clf()
    return uploaded_image.link