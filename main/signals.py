from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

import os

from .models import Profil, Playlist

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@receiver(post_save, sender=User)
def create_playlist(sender, instance, created, **kwargs):
    if created :
        Profil.objects.create(
            name=instance.username,
            email=instance.email,
            user=instance
        )

        Playlist.objects.create(
            title='Watch list',
            creator=instance
        )

@receiver(pre_save, sender=Profil)
def delete_prev_img(sender, instance, update_fields=None, **kwargs):
    try :
        new_img = str(instance.avatar_img)
        prev_img = str(Profil.objects.get(pk=instance.uid).avatar_img)

        if new_img != prev_img and prev_img != 'default.png':
            path = os.path.join(BASE_DIR, 'static\images', prev_img)
            if os.path.exists(path) :
                os.remove(path)

            if new_img == '' :
                instance.avatar_img = 'default.png'

    except :
        pass