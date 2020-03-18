from django.db import models
from django.contrib.auth.models import User

import uuid

# Create your models here.
class Profil(models.Model) :
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta :
        constraints = [
            models.UniqueConstraint(fields=['user'], name='user_unique_profil'),
            models.UniqueConstraint(fields=['email'], name='email_unique_profil')
        ]

    def __str__(self) :
        return self.name

class Playlist(models.Model) :
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=200, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta :
        constraints = [
            models.UniqueConstraint(fields=['creator', 'title'], name='one_playlist_for_each_user')
        ]

class PlaylistItem(models.Model) :
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    item = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)