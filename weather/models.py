from django.db import models

from django.contrib.auth.models import User


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    station_id = models.IntegerField()
    name = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    def __str__(self):
        if self.name:
            return f'{self.user.username}-{self.name}'
        return f'{self.user.username}-{self.station_id}'
    def get_serializable(self):
        '''returns all fields except user foreign key'''
        return {
            'station_id':self.station_id,
            'name':self.name,
            'latitude':self.latitude,
            'longitude':self.longitude
        }


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True, blank=True, unique=True)
    def __str__(self):
        return f'{self.user.username} Profile'