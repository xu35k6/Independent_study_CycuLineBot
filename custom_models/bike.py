import requests


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
        # print(response.status_code)
        # print(response.json())
        return response.json()['access_token']

    def get_response(self, url):
        headers = {'authorization': f'Bearer {self.get_token()}'}
        response = requests.get(url, headers=headers)
        return response.json()


def bike():
    tdx = TDX(client_id, client_secret)

    base_url = "https://tdx.transportdata.tw/api/basic/v2/Bike"
    bike_url = "/City/Taoyuan"

    url = f"{base_url}{'/Station'}{bike_url}?%24format=JSON"
    response_Station = tdx.get_response(url)
    
    station = ['TAO2005','TAO2004','TAO2012','TAO2254']
    hasbike = [False,False,False]
    #TAO2005:中原大學, TAO2004 : 中壢車站前站  ,TAO2012 : 中壢車站後站, TAO2254 : 大潤發中壢店
    j = 0
    class Bike:
        Name = []
        Rent = []
        Return = []
        google_map = []
    U_bike = Bike
    temp = []
    for No in station:
        for i in range(len(response_Station)):
            if response_Station[i]['StationUID'] == No:
                U_bike.Name.append(response_Station[i]['StationName']['Zh_tw'])
        url = f"{base_url}{'/Availability'}{bike_url}?%24format=JSON"
        response_Availability = tdx.get_response(url)
        
        for i in range(len(response_Availability)):
            if response_Availability[i]['StationUID'] == No:
                U_bike.Rent.append(response_Availability[i]['AvailableRentBikes'])
                U_bike.Return.append(response_Availability[i]['AvailableReturnBikes'])
                U_bike.google_map.append(f"{'https://www.google.com/maps/place/'}{response_Station[i]['StationPosition']['PositionLat']}{'+'}{response_Station[i]['StationPosition']['PositionLon']}")
    return U_bike

if __name__ == '__main__':
    U_bike = bike()
    from pprint import pprint
    pprint(U_bike.Name+U_bike.google_map)





   
