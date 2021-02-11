import requests

class WeatherApi:
    '''WeatherApi(api_key, url)'''
    def __init__(self, key):
        
        self.url = "https://api.openweathermap.org/data/2.5/"
        self.key = key

    def current(self,**kwargs):
        url = self.url+'weather'
        data = {'appid':self.key}
        if 'id' in kwargs.keys():
            data['id'] = kwargs['id']
        elif set(['lat','lon']).issubset(kwargs):
            data['lat'] = kwargs['lat']
            data['lon'] = kwargs['lon']
        else:
            return {'cod':404}
        response = requests.get(url, data)
        return response
    
    def find(self, lat, lon, count):
        url = self.url+'find'
        data = {
            'appid':self.key,
            'lat':lat,
            'lon':lon,
            'cnt':count
            }
        response = requests.get(url,data)
        return response