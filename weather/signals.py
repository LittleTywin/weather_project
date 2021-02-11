from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from .models import Profile

## import to apps.py

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    try:
        profile=instance.profile
    except :
        profile = Profile.objects.create(user=instance)
    profile.save()
    