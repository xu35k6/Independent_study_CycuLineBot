from numpy import uint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
from lxml import html
from bs4 import BeautifulSoup
from pprint import pprint


def Booktype():
    try:
        purpose = input("請問您想找參考書還是教科書呢?")
        #C:\python\圖書館搜尋\參考書(含名稱).csv
    except:
        print('輸入錯誤，再試一次')
        purpose = Booktype()
    return purpose

def Searchbook(classnum,purpose,booknum):
    find = False
    i = 1
    searchpurpose = '0'
    for Booknum in booknum["課程代碼"] :
        i +=1
        j = 1
        f = 1
        if classnum == Booknum:
            print("已為您搜尋課程:",booknum['課程名稱'][i-2])
            if str(booknum[purpose+ str(j)][i-2]) != 'nan' and j<41:
                print("以下為教授提供的"+purpose+'清單:')
                while str(booknum[purpose+ str(j)][i-2]) != 'nan' and j<41:
                    print(j,":",booknum[purpose+ str(j)][i-2])
                    j+=1
                f = input('請問您想搜尋第幾本書呢?')
                while int(f)>= int(j):
                    f = input('輸入錯誤\n請問您想搜尋第幾本書呢?')
                searchpurpose = booknum[purpose + str(f)][i-2]
            break
    if str(booknum[purpose+ str(f)][i-2]) == 'nan':
        print("老師沒公布"+ purpose +"QQ")
    else:
        print('\n已為您搜尋--------'+ purpose +":"+ str(searchpurpose))
    
    return searchpurpose

def Classnum(classnum,purpose):
    booknum = pd.read_csv('/app/other/' + purpose + '1111.csv')#C:\python\python-training\圖書館搜尋\參考書(含名稱).csv
    book = []
    class_name = ""
    find = False
    for i in range(len(booknum['課程代碼'])):
        if booknum['課程代碼'][i] == classnum:
            book.append(booknum['課程名稱'][i])
            find = True
            for j in range(41):
                if str(booknum[purpose+ str(j+1)][i]) != 'nan':
                    book.append(booknum[purpose+ str(j+1)][i])
            break
    return book

# https://cylis.lib.cycu.edu.tw/search~S1*cht/?searchtype=Y&searcharg=%E6%B0%91%E6%B3%95%E6%A6%82%E8%AB%96&searchscope=1&sortdropdown=-&SORT=DZ&extended=1&SUBMIT=%E6%9F%A5%E8%A9%A2&searchlimits=&searchorigarg=Y%7Bu6C11%7D%7Bu6CD5%7D%7Bu7269%7D%7Bu6B0A%7D%26SORT%3DD
# https://cylis.lib.cycu.edu.tw/search~S1*cht/?searchtype=Y&searcharg=%E6%B0%91%E6%B3%95%E6%A6%82%E8%AB%96&searchscope=1&sortdropdown=-&SORT=DZ&extended=1&SUBMIT=%E6%9F%A5%E8%A9%A2&searchlimits=&searchorigarg=Y%7Bu6C11%7D%7Bu6CD5%7D%7Bu6982%7D%7Bu8AD6%7D%26SORT%3DDZ
def request_find(searchbook):
    url = f'https://cylis.lib.cycu.edu.tw/search*cht/~?searchtype=Y&SORT=D&searcharg='+searchbook#+'&availlim=1'
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36'
        # 'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
    }

    r = requests.get(url, allow_redirects = False, headers = headers ) # 取得畢業門檻-修課紀錄
    soup = BeautifulSoup(r.text, 'lxml')
    soup.encoding = 'utf-8'

    status = ['可外借','到期','已註銷','在預約保留架上','剛歸還，尚待上架','擬購中','暫不公開','編目中','不予採購','填寫線上調閱單','書庫點收中','新書展示中','下落不明','遺失且未繳款','公務用書','教師專案用書','擬淘汰','依各系規定','待尋中','傳回本館中','限館內使用','磁片損壞','宣稱還書','遺失賠償','填調閱單']

    book_name = soup.find_all(class_ = 'briefcitTitle') #架上情況:class_='bibItemsEntry'
    name_content = [] 
    for b in book_name:       
        stem = b.text
        stem = stem.strip()
        name_content.append( stem )
    
    name_content1 = [] 
    if name_content == []:
        bib_name = soup.find_all(class_='bibInfoData')
        for name in bib_name:       
            stem = name.text
            stem = stem.strip('\n')
            name_content1.append( stem )
    if name_content1 == [] and name_content == []:
        print("找不到此書")
        return []
    bibItemsEntry = soup.find_all(class_='bibItemsEntry') #架上情況:class_='bibItemsEntry'
    bib_content = [] 
    for bib in bibItemsEntry:       
        stem = bib.text
        stem = stem.strip(' ')
        stem = stem.strip('\n')
        stem = stem.strip('\xa0')
        stem = stem.replace('xa','')
        stem = stem.replace('','')
        stem = stem.replace('xa0','')
        stem = stem.replace('\n','')
        bib_content.append( stem.split("\xa0") )
    pprint(bib_content)

    temp = soup.find_all('a') #書名和書號
    temp_content = [] 
    num = 0
    for i in range(len(temp)):
        num += 1       
        stem = temp[i].text
        stem = stem.strip()
        if stem == "(說明)":
            if temp[i-2].text == '':
                temp_content.append( [temp[i-3].text,temp[i+2].text] )
            elif temp[i+2].text == '' or temp[i+2].text == ' ':
                temp_content.append( [temp[i-2].text,temp[i+1].text] )
            else:
                temp_content.append( [temp[i-2].text,temp[i+2].text] )
    pprint(temp_content)

    res = []
    now = []
    output = False
    book_num = 0
    if name_content !=[]:
        for i in range(len(temp_content)) :
            now = []
            for j in range(len(bib_content)):
                for k in range(len(bib_content[j])):
                    if temp_content[i][1] != ' ' and temp_content[i][1] != '' and temp_content[i][1] in bib_content[j][k]:
                        for l in range(len(bib_content[j])):
                            for m in range(len(status)):
                                if status[m] in bib_content[j][l] :
                                    if status[m] == '已註銷':
                                        now.append(['已註銷',bib_content[j][l]])
                                    else:
                                        print(temp_content[i][0],bib_content[j][0],bib_content[j][l])
                                        now.append([bib_content[j][0],bib_content[j][l]])#地點、狀態
                                        break
                                    book_num +=1
            res.append([temp_content[i][0],now])
            # pprint(res)




    else :
        for i in range(len(bib_content)):
            for l in range(len(bib_content[i])):
                for m in range(len(status)):
                    if status[m] in bib_content[i][l] :
                        if status[m] == '已註銷':
                            now.append(['已註銷',bib_content[i][l]])
                        else:
                            now.append([bib_content[i][0],bib_content[i][l]])
                        book_num +=1
        res.append([name_content1[2],now])
            

    # print(len(bib_content),book_num,len(temp_content))
    return res

if __name__ == '__main__':
    # purpose = Booktype()#先問要找教科書/參考書
    # classnum,book,find = Classnum(purpose)#再問課程代碼
    # print(book)
    # if find:
    #     searchbook = Searchbook(classnum,purpose,book)#再問哪本書
    #     if searchbook != '0' :
    #         res = request_find(searchbook)
    # else :
    #     print("課程代碼輸入錯誤")
    # res = request_find('民法總則')
    # if len(res) > 10:
    #     res = res[:10]
    # for i in range(len(res)):
    #     print(res[i][0])
    #     for j in range(len(res[i])-1):
    #         for k in range(len(res[i][j+1])):
    #             print(res[i][j+1][k][0],res[i][j+1][k][1],'\n')
    request_find("Introduction to Data Mining")