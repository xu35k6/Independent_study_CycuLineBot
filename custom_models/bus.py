import requests
import pandas as pd
from math import cos, sin, radians, asin, sqrt

client_id = ''
client_secret = ''


class TDX():
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_token(self):
        token_url = 'https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token'
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(token_url, headers=headers, data=data)

        return response.json()['access_token']

    def get_response(self, url):
        headers = {'authorization': f'Bearer {self.get_token()}'}
        response = requests.get(url, headers=headers)
        return response.json()

import time
def Get_bus(num):
    tdx = TDX(client_id, client_secret)
    base_url = "https://tdx.transportdata.tw/api"
    endpoint = "/basic/v2/Bus/EstimatedTimeOfArrival/City/Taoyuan/"
    OriginStationID = num
    start = time.time()
    url = f"{base_url}{endpoint}{OriginStationID}?$24format=JSON"
    response = tdx.get_response(url)
    if len(response) == 0:
        print('查無此班次資料')
        quit()
    get = time.time()
    class Bus1:
        num = []
        time = [] 
        name = []
    class Bus0:
        num = []
        time = [] 
        name = []
        
    bus_1 = Bus1()
    for i in range(len(response)):
        for j in range(len(response)):
            if response[j]['Direction'] == 1:
                if response[j]['StopSequence'] == i:
                    if response[j]['StopSequence'] not in bus_1.num:
                        bus_1.num.append(response[j]['StopSequence'])
                        bus_1.name.append(response[j]['StopName']['Zh_tw'])
                        try:
                            bus_1.time.append('預計再過'+str(round(response[j]['Estimates'][0]['EstimateTime']/60))+'分進站')
                        except:
                            try:
                                bus_1.time.append('預計'+response[j]['NextBusTime'][11:16]+'進站')
                            except:
                                bus_1.time.append( '休息')
    bus_0 = Bus0()
    for i in range(len(response)):
        for j in range(len(response)):
            if response[j]['Direction'] == 0:
                if response[j]['StopSequence'] == i:
                    if response[j]['StopSequence'] not in bus_0.num:
                        bus_0.num.append(response[j]['StopSequence'])
                        bus_0.name.append(response[j]['StopName']['Zh_tw'])
                        try:
                            bus_0.time.append('預計再過'+str(round(response[j]['Estimates'][0]['EstimateTime']/60))+'分進站')
                        except:
                            try:
                                bus_0.time.append('預計'+response[j]['NextBusTime'][11:16]+'進站')
                            except:
                               bus_0.time.append( '休息')
    end = time.time()
    print('車次',num,'request:',get-start,' 計算:', end - get)
    return [bus_0,bus_1]

def min_distance_25(origins_Longitude,origins_Latitude,first):
    station = pd.read_csv('/app/other/公車座標.csv')
    min_25 = []
    for i in range(3361):
        dlat = origins_Latitude - station['緯度'][i]
        dlon = origins_Longitude - station['經度'][i]
        distance = ( 6371 * 2 * asin(sqrt((sin(dlat/2)**2 + cos(origins_Latitude) * cos(station['緯度'][i]) * sin(dlon/2)**2 ))))*1.609344/100*1000
        min_25.append([distance,station['站名'][i],station['座標'][i],station['緯度'][i],station['經度'][i]])

    min_25.sort()
    min_25 = min_25[first:]
    temp_station = []
    log_lat = []
    for i in range(1):
        temp_station.append(min_25[i][1])
        log_lat.append(min_25[i][2])
    return temp_station, log_lat

def bus_Nearest(lat,log,first):
    location,log_lat = min_distance_25(log,lat,first)
    route = pd.read_csv('/app/other/公車站行駛路線.csv')
    num = []
    res = []
    num_temp = []
    route_temp = []
    for k in range(len(location)):
        rou = []
        for i in range(len(route['站名'])):
            if route['站名'][i] == location[k]:
                for j in range(44):
                    if str(route['路線'+str(j+1)][i]) == 'nan':
                        break 
                    if route['路線'+str(j+1)][i] not in num:
                        num.append(route['路線'+str(j+1)][i])

        for i in range(len(num)):
            if num[i] not in num_temp:
                num_temp.append(num[i])
                bus_0,bus_1 = Get_bus(num[i])
                route_temp.append([num[i],bus_0,bus_1])
                for j in range(len(bus_1.name)):
                    if bus_1.name[j] == location[k]:
                        rou.append([str(num[i]),bus_1.time[j],bus_1.name[len(bus_1.name)-1]])

                for j in range(len(bus_0.name)):
                    if bus_0.name[j] == location[k]:
                        rou.append([str(num[i]),bus_0.time[j],bus_0.name[len(bus_0.name)-1]])
            else:
                print(num[i])
                for l in range(len(route_temp)):
                    if num[i] == route_temp[l][0]:
                        for j in range(len(route_temp[l][2].name)):
                            if route_temp[l][2].name[j] == location[k]:
                                rou.append([str(num[i]),route_temp[l][2].time[j],route_temp[l][2].name[len(route_temp[l][2].name)-1]])

                        for j in range(len(route_temp[l][1].name)):
                            if route_temp[l][1].name[j] == location[k]:
                                rou.append([str(num[i]),route_temp[l][1].time[j],route_temp[l][1].name[len(route_temp[l][1].name)-1]])

        res.append([location[k],rou])
    return location,res,log_lat




   
