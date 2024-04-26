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
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False
# plt.rcParams['font.sans-serif'] = ['jf-openhuninn-1.1']




def Count( db, className, teacherName, classCode ) :
    collection = db['課程評價']
    comment = collection.find_one({ "課程名稱" : className, "老師名稱" : teacherName, "課程代碼" : classCode })
    if comment != None :
        s1 = 0
        s2 = 0
        s3 = 0
        s4 = 0
        for i in range( len( comment['UserID'] ) ) :
            s1 += int( comment['作業量分數'][i] )
            s2 += int( comment['課程難度分數'][i] )
            s3 += int( comment['學到東西分數'][i] )
            s4 += int( comment['給分甜不甜分數'][i] )
        s1 = s1 * 100 / ( 5 * len( comment['UserID'] ) )
        s2 = s2 * 100 / ( 5 * len( comment['UserID'] ) )
        s3 = s3 * 100 / ( 5 * len( comment['UserID'] ) )
        s4 = s4 * 100 / ( 5 * len( comment['UserID'] ) )
        toReturn = []
        toReturn.append( s1 )
        toReturn.append( s2 )
        toReturn.append( s3 )
        toReturn.append( s4 )
        return toReturn
    else :
        return None