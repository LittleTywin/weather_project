from django.shortcuts import render,redirect,reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from  django.conf import settings
import json
from .weather_api import WeatherApi
from .models import Location
import flag
from . import wind




def home(request):
    data = {}
    if request.user.is_authenticated:
        default_location = request.user.profile.default_location
        if default_location:
            weather_api = WeatherApi(settings.WEATHER_API_KEY)
            response_data = weather_api.current(id=default_location.station_id)
            data = response_data.json()
            icon = data['weather'][0]['icon']
            data['main']['temp'] = round(data['main']['temp']-273.15)
            data['main']['feels_like'] = round(data['main']['feels_like']-273.15)
            data['weather'][0]['icon'] = f'https://openweathermap.org/img/wn/{icon}@2x.png'
            data['sys']['emoji'] = flag.flag(data['sys']['country'])
            data['visibility'] /=1000
            data['wind']['dir'] = wind.degrees_to_direction(data['wind']['deg'])
    return render(request, 'weather/home.html', {'data':data})


@login_required
def profile(request):
    if request.is_ajax():
        sposition = request.POST.get('position')
        count = request.POST.get('count')

        if sposition and count:
            position = json.loads(sposition)
            weather_api = WeatherApi(settings.WEATHER_API_KEY)
            response = weather_api.find(lon=position['longitude'], lat=position['latitude'], count=count)
            response_list = response.json()['list']
            data = []
            for idx,location in enumerate(response_list):
                location_data={}
                location_data['id'] = location.get('id', None)
                location_data['name'] = location.get('name', None)
                location_data['coord'] = location.get('coord', None)
                data.append(location_data)
            print(data)
            return JsonResponse({'nearby_locations':json.dumps(data)},status=200) 

        return JsonResponse({'error':'bad request'}, status=200)    
    #GET
    locations = list(request.user.location_set.all().values('station_id','name','latitude','longitude'))
    default_location= request.user.profile.default_location
    data = {}
    if default_location:
        data['default_location']= default_location.get_serializable()
    data['locations'] = locations
    
    return render(request, 'weather/profile.html', data)

@login_required
def new_location(request, station_id):
    weather_api = WeatherApi(settings.WEATHER_API_KEY)
    new_location = weather_api.current(id=station_id).json()
    location = Location(
        user = request.user,
        station_id = station_id,
        name = new_location.get('name'),
        latitude = new_location.get('coord').get('lat'),
        longitude = new_location.get('coord').get('lon')
    )
    location.save()
    return redirect(reverse('weather:profile'))

@login_required
def delete_location(request, station_id):
    location = get_object_or_404(Location, station_id=station_id, user = request.user)
    location.delete()
    return redirect(reverse('weather:profile'))

@login_required
def set_default(request, station_id):
    location = get_object_or_404(Location, station_id=station_id, user = request.user)
    request.user.profile.default_location = location
    print(location)
    request.user.save()
    return redirect(reverse('weather:home'))

def url_not_found(request):
    return redirect(reverse('weather:home'))