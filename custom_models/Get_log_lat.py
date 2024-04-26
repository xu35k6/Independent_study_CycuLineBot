import requests
from bs4 import BeautifulSoup

def Get_log_lat(destinations):
    url = 'https://www.google.com/maps/place?q='+ destinations
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.prettify()
    initial_pos = text.find(";window.APP_INITIALIZATION_STATE")
        #尋找;window.APP_INITIALIZATION_STATE所在位置
    data = text[initial_pos+36:initial_pos+85] #將其後的參數進行存取
    line = tuple(data.split(','))
    num1 = float(line[1])
    num2 = float(line[2])
    a = []
    a.append([num2,num1])
    return a 

if __name__ == '__main__':
    a = Get_log_lat('桃園機場')
    print(a)