import pymongo
import pandas as pd

client = pymongo.MongoClient("")
db = client.test # 選擇database

# food = db['口味/食物種類']
# restaurant = db['餐廳名稱']
# menu = db['菜單']

list1 = []
list2 = []
list3 = []

df = pd.read_excel('menu_info_dinner(Monday).xlsx',usecols=[0])
list1 = df['口味/品項']
df = pd.read_excel('menu_info_dinner(Monday).xlsx',usecols=[1])
list2 = df['餐廳名稱']
df = pd.read_excel('menu_info_dinner(Monday).xlsx',usecols=[2])
list3 = df['菜單']

collection = db['menu_info']

# print(list3[0])
i = 0
while i < len(list1):
    print(i)
    menu = []
    temp = collection.find_one({ '口味/品項':list1[i],'餐廳名稱':list2[i] }) 
    if(temp == None):
        menu.append(list3[i])
        data = {'口味/品項':list1[i],'餐廳名稱':list2[i],'菜單':menu}
        collection.insert_one(data)
    else:
        temp['菜單'].append(list3[i])
        collection.update_one({ '口味/品項':list1[i], '餐廳名稱':list2[i] },{ "$set" : { '菜單' : temp['菜單'] } })
    i+=1
    