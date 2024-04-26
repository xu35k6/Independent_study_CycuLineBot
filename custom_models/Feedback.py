'''https://www.learncodewithmike.com/2020/02/python-email.html'''

'''回饋意見用，此function將使用者的回饋(contents)寄信到mimolinebot的gmail中'''

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def Feedback( contexts ) :
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = "意見回饋/問題回報"  #郵件標題
    content["from"] = ""  #寄件者
    content["to"] = "" #收件者
    content.attach(MIMEText(contexts) )  #郵件內容


    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("", '')  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
        except Exception as e:
            print("Error message: ", e)




