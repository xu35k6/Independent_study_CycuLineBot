from ast import walk
from math import cos
from pprint import pprint
import pandas as pd
import requests
from math import cos, sin, radians, asin, sqrt
import time

from custom_models import Get_log_lat, bus,Transfer
google_key = ''

#用google_map_api找出步行距離最近的10個站點
def google_api(origins_Longitude,origins_Latitude,min_25):
    destinations = min_25[0][0]
    origins = str(origins_Latitude) + '+' + str(origins_Longitude)
    i = 1
    while(i<len(min_25)-1):
        destinations += '%7C'
        destinations += min_25[i][0]
        i+=1
    
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?mode=walking&origins={origins}&destinations={destinations}&units=METRIC&key={google_key}"
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    min_10 = []
    #response.json()['rows'][0]['elements'][i]['duration']['value']是步行時間
    for i in range(len(min_25)-1):
        min_10.append([(response.json()['rows'][0]['elements'][i]['distance']['value']),min_25[i][1],min_25[i][0]])
    min_10.sort()
    return min_10

#找出直線距離最近的25個站點
def min_distance_25(origins_Longitude,origins_Latitude):
    # print('找直線距離')
    station = pd.read_csv('/app/other/公車座標.csv',low_memory=False)
    # print('公車座標讀取成功')
    min_25 = []
    for i in range(3361):
        dlat = origins_Latitude - station['緯度'][i]
        dlon = origins_Longitude - station['經度'][i]
        distance = ( 6371 * 2 * asin(sqrt((sin(dlat/2)**2 + cos(origins_Latitude) * cos(station['緯度'][i]) * sin(dlon/2)**2 ))))*1.609344/100*1000
        min_25.append([distance,station['站名'][i],station['座標'][i],station['緯度'][i],station['經度'][i]])

    min_25.sort()
    temp = []
    temp_station = []
    for i in range(25):
        if min_25[i][0] < 700:
            temp_station.append(min_25[i][1])
            temp.append([min_25[i][2],min_25[i][1],min_25[i][0]])
        else:
            break
    print(len(temp))
    return temp_station,temp   
    
#找出該站所經過的所有公車
def has_bus(bus_station):
    all_bus = pd.read_csv("/app/other/公車站行駛路線.csv")
    bus_now = []
    bus_total = {}
    route = []
    for k in range(len(bus_station)):
        bus_now = []
        for i in range(len(all_bus['站名'])):
            j = 1
            if ( bus_station[k][1] == all_bus['站名'][i]):
                while(str(all_bus['路線'+str(j)][i]) != 'nan' and j < 44):
                    if all_bus['路線'+str(j)][i] not in bus_now:
                        if all_bus['路線'+str(j)][i] not in route:
                            bus_now.append(all_bus['路線'+str(j)][i])
                            route.append(all_bus['路線'+str(j)][i])
                    j+=1
                bus_total[str(bus_station[k][1])] = bus_now
    return bus_total

#不含步行資訊
def min_distance(o_bus,o_min_10,d_bus,d_min_10,first_num):
    start = time.time()
    temp = list(o_bus.keys()) #起點的所有站名
    bus_temp = []
    bus_time = ''
    min_distance_final = ''
    class Route:
        origin_station = []
        end_station = []
        walk_dis_1 = []
        walk_dis_2 = []
        route_name = []
        time = []
        stop_num = []
        log_lat = []
    result = Route()
    bus_num = 0
    this_num = 0
    for i in range(len(temp)):
        for j in range( len( o_bus[temp[i]] ) ):
            if o_bus[temp[i]][j] not in bus_temp:
                for k in range( len(list(d_bus.values()))):
                    #如果起終點公車路線重疊，將起點站存於bus_temp
                    if ( o_bus[temp[i]][j] in list(d_bus.values())[k] ):
                        bus_temp.append(o_bus[temp[i]][j])
                        #獲取公車即時時間
                        #bus1和bus0分別代表一個方向，若是單一方向僅會有bus0有資料
                        bus_num += 1
                        if bus_num >= first_num:
                            bus1,bus0  = bus.Get_bus(o_bus[temp[i]][j])
                            #用兩個for迴圈判斷起點至終點屬於哪個方向
                            #如果先讀到起點就存下來，然後break，若是先讀到終點就換讀下一個方向
                            has_a = False
                            has = False
                            num = 0
                            for a in range(len(bus1.name)):
                                if bus1.name[a] == temp[i]:
                                    bus_time = bus1.time[a]
                                    has = True
                                    num = bus1.num[a]
                                elif bus1.name[a] == list(d_bus.keys())[k]:
                                    if has :
                                        has_a = True
                                        num = bus1.num[a] - num
                                    break
                            if not has_a:
                                for b in range(len(bus0.name)):
                                    if bus0.name[b] == temp[i]:
                                        bus_time = bus0.time[b]
                                        num = bus0.num[b]
                                    elif bus0.name[b] == list(d_bus.keys())[k]:
                                        num = bus0.num[b] - num
                                        break
                            #如果該班車能從起點到終點，則存於final，有些公車路線會經過起終點，但是是從終點往起點行駛。
                            if str(bus_time) != '休息' and str(bus_time) != '':
                                this_num += 1
                                result.origin_station.append(temp[i])
                                result.end_station.append(list(d_bus.keys())[k]) 
                                result.route_name.append(str(o_bus[temp[i]][j])) 
                                result.time.append(str(bus_time)) 
                                result.stop_num.append(str(num)) 
                                result.log_lat.append(o_min_10[i][0])
                                result.walk_dis_1.append(str(round(o_min_10[i][2])))
                                for h in range(len(d_min_10)):
                                    if list(d_bus.keys())[k] == str(d_min_10[h][1]):
                                        result.walk_dis_2.append(str(round(d_min_10[h][2])))
                                        walk_dis_2 = d_min_10[h][2]
                                min_distance_final = ('步行 '+str(round(o_min_10[i][2]))+' 公尺，前往'+temp[i]+'搭乘:'+str(o_bus[temp[i]][j])+'號公車:'+str(bus_time)+'經過'+str(num-1)+'站，抵達'+list(d_bus.keys())[k]+'下車，後步行 '+ str(round(walk_dis_2))+' 公尺抵達'+'\n')
                                print(min_distance_final)
                                bus_time = ''
                                end = time.time()
                                if round(end-start) > 20 or this_num == 3:
                                    return result
                                break
                        
    return result

#含步行距離資訊
def now_min_distance(o_bus,o_min_10,d_bus,d_min_10,first_num):
    start = time.time()
    temp = list(o_bus.keys())
    bus_temp = []
    bus_time = ''
    class Route:
        origin_station = []
        end_station = []
        walk_dis_1 = []
        walk_dis_2 = []
        route_name = []
        time = []
        stop_num = []
        log_lat = []
    result = Route()
    this_num = 0
    bus_num = 0
    for i in range(len(temp)):
        for j in range( len( o_bus[temp[i]] ) ):
            for k in range( len(list(d_bus.values()))):
                if o_bus[temp[i]][j] in bus_temp:
                    None
                elif ( o_bus[temp[i]][j] in list(d_bus.values())[k] ):
                    bus_temp.append(o_bus[temp[i]][j])
                    bus_num += 1
                    if bus_num > first_num:
                        #獲取公車即時時間
                        #bus1和bus0分別代表一個方向，若是單一方向僅會有bus0有資料
                        bus1,bus0  = bus.Get_bus(o_bus[temp[i]][j])
                        num = 0
                        a_has = False
                        has = False
                        
                        #用兩個for迴圈判斷起點至終點屬於哪個方向
                        #如果先讀到起點就存下來，然後break，若是先讀到終點就換讀下一個方向
                        for a in range(len(bus1.name)):
                            if bus1.name[a] == temp[i]:
                                has = True
                                bus_time = bus1.time[a]
                                num = bus1.num[a]  
                                
                            elif bus1.name[a] == list(d_bus.keys())[k]:
                                num = bus1.num[a] - num
                                if has :
                                    a_has = True
                                break
                        if not a_has:
                            for b in range(len(bus0.name)):
                                if bus0.name[b] == temp[i]:
                                    num = bus0.num[b]  
                                    bus_time = bus0.time[b]
                                    
                                elif bus0.name[b] == list(d_bus.keys())[k]:
                                    num = bus0.num[b] - num
                                    break
                            #如果該班車能從起點到終點，則存於final，有些公車路線會經過起終點，但是是從終點往起點行駛。
                        if  bus_time != '' and bus_time != '休息' and temp[i] != list(d_bus.keys())[k]:#
                            # print("!!!!!!!!!!!!!!!!!!",o_min_10)
                            this_num += 1
                            result.origin_station.append(temp[i])
                            result.end_station.append(list(d_bus.keys())[k]) 
                            result.walk_dis_1.append(str(o_min_10[i][0])) 
                            walk_dis_2 = ''
                            for h in range(len(d_min_10)):
                                if list(d_bus.keys())[k] == str(d_min_10[h][1]):
                                    walk_dis_2 = str(d_min_10[h][0])
                                    result.walk_dis_2.append(str(d_min_10[h][0])) 
                            result.route_name.append(str(o_bus[temp[i]][j])) 
                            result.time.append(str(bus_time)) 
                            result.stop_num.append(str(num)) 
                            result.log_lat.append(o_min_10[i][2])
                            print('步行'+str(o_min_10[i][0])+'公尺，前往'+temp[i]+'搭乘:'+str(o_bus[temp[i]][j])+'號公車:'+str(bus_time)+'經過'+str(num-1)+'站前往'+list(d_bus.keys())[k]+'後步行'+walk_dis_2+'公尺，後抵達'+'\n')

                            num = 0
                            bus_time = ''
                            end = time.time()
                            if round(end-start) > 20 or this_num == 3:
                                return result
                            break 
                        # result.origin_station.append(temp[i])
                        # result.end_station.append(list(d_bus.keys())[k]) 
                        # result.walk_dis_1.append(str(o_min_10[i][0]))
                        # for h in range(len(d_min_10)):
                        #     if list(d_bus.keys())[k] == str(d_min_10[h][1]):
                        #         result.walk_dis_2.append(str(d_min_10[h][0]))
                        # result.route_name.append(str(o_bus[temp[i]][j])) 
                        # result.time.append(str(bus_time)) 
                        # result.stop_num.append(str(0)) 
                        # result.log_lat.append(o_min_10[i][0])
                        # bus_time = ''
                        # break
    return result

# FIXME 行程錯誤
def Get_min_distance(origin,destinations,first_num):
    print('Get_min_distance!')
    #未來用line抓位置，現用中原大學的位置
    origins_Longitude = origin[1]
    origins_Latitude = origin[0]
    #設定終點經緯度
    destinations_Longitude = destinations[1]
    destinations_Latitude = destinations[0]
    print('設定完座標')
    #先算出當前直線距離最近的25個站點
    o_min_line = []
    d_min_line = []
    o_temp_station = []
    d_temp_station = []
    (o_temp_station,o_min_line) = min_distance_25(origins_Longitude,origins_Latitude)
    (d_temp_station,d_min_line) = min_distance_25(destinations_Longitude,destinations_Latitude)

    # #計算行程
  
    # #無步行距離的行程計算
    min_distance_final = ''
    # #找出這25個站點有的公車路線
    # o_bus = has_bus(o_min_line)
    # d_bus = has_bus(d_min_line)

    # min_distance_final = min_distance(o_bus,o_min_line,d_bus,d_min_line,first_num)

    #含步行距離的行程計算

    #用google_map_api找出步行距離最近的25個站點
    o_min_walk = google_api(origins_Longitude,origins_Latitude,o_min_line)
    d_min_walk = google_api(destinations_Longitude,destinations_Latitude,d_min_line)

    o_bus = has_bus(o_min_walk)
    d_bus = has_bus(d_min_walk)

    min_distance_final = now_min_distance(o_bus,o_min_walk,d_bus,d_min_walk,first_num)

    # if min_distance_final.route_name == []:
        # min_distance_final = Tranfer.tranfer(o_temp_station,d_temp_station) 

    # print( 'min_distance:', format(end1-start),'\n'+'tranfer:',end-end1) 
    return min_distance_final




