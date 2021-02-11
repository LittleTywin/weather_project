from django.contrib import admin

# Register your models here.
from .models import Location, Profile

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    pass