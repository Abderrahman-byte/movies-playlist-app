from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profil, Playlist

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