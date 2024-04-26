from numpy import uint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import pandas as pd
import pickle

def GetMySelf(id,password) :
    # #driver
    # options = Options()
    # #最大化
    # options.add_argument("start-maximized")
    # #不加載圖片
    # options.add_argument('blink-settings=imagesEnabled=false') 
    # #最大權限運作
    # options.add_argument('--no-sandbox')
    # #避免彈出式視窗
    # prefs = {  
    #     'profile.default_content_setting_values' :  {  
    #         'notifications' : 2  
    #     }  
    # }  

    # options.add_experimental_option('prefs',prefs)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # options.add_argument('User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless") #無頭模式
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    driver.get("https://myself.cycu.edu.tw/#/life/elective_system")
    #login
    WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))
                )
    account = driver.find_element(By.XPATH,'//*[@id="username"]').send_keys(id)
    pwd = driver.find_element(By.XPATH,'//*[@id="pwd"]').send_keys(password)
    login_bth = driver.find_element(By.XPATH,'//*[@id="login"]/div/div[2]/form/div[3]/input')
    driver.execute_script("arguments[0].click();", login_bth)

    #course
    WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="indexContent"]/div/div[2]/div[4]/div/div/h5'))
                )
    
    course_selection = driver.find_element(By.XPATH,'//*[@id="indexContent"]/div/div[2]/div[4]/div/div')
    driver.execute_script("arguments[0].click();", course_selection)
    WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="page-content-wrapper"]/div/div[5]/table/tbody/tr[1]/td[3]'))
                )
    i = 1
    t = True
    num = []
    try:
        while(t):
            course_year = driver.find_element(By.XPATH,'//*[@id="page-content-wrapper"]/div/div[5]/table/tbody/tr['+str(i)+']/td[2]')
            course_num = driver.find_element(By.XPATH,'//*[@id="page-content-wrapper"]/div/div[5]/table/tbody/tr['+str(i)+']/td[3]')
            course_name = driver.find_element(By.XPATH,'//*[@id="page-content-wrapper"]/div/div[5]/table/tbody/tr['+str(i)+']/td[4]')
            course_credit = driver.find_element(By.XPATH,'//*[@id="page-content-wrapper"]/div/div[5]/table/tbody/tr['+str(i)+']/td[7]') 
            course_score = driver.find_element(By.XPATH,'//*[@id="page-content-wrapper"]/div/div[5]/table/tbody/tr['+str(i)+']/td[8]') 
            s = course_year.text
            if s[0] == '#' :
                s = s[1:]
            # print('course_score.text:',course_score.text)
            if course_score.text != '' :
                num.append([s,course_num.text,course_name.text,course_credit.text,course_score.text])
            i = i + 1
    except:
        return num