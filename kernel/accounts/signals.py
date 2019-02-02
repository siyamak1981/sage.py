from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from .models import Profile
from .models import Role

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        role = Role.objects.get(title='default')
    except:
        role = Role.objects.create(title='default', description='default user')
    
    if created:
        Profile.objects.create(user=instance, role=role)
    instance.profile.save()


