from django.db import models
from django.contrib.auth.models import User

import uuid

# Create your models here.
class Profil(models.Model) :
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    avatar_img = models.ImageField(null=True, blank=True)
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
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta :
        constraints = [
            models.UniqueConstraint(fields=['creator', 'title'], name='one_playlist_for_each_user')
        ]

    def __str__(self) :
        return f'{self.title} by {self.creator.username}'

class PlaylistItem(models.Model) :
    MEDIA_TYPE = (
        ('movie', 'Movie'),
        ('tv', 'Tv Show')
    )

    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    item_id = models.CharField(max_length=200)
    media_type = models.CharField(max_length=200, choices=MEDIA_TYPE, default='movie')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['playlist', 'item_id', 'media_type'], name='non_duplicate_items_in_playlist')
        ]
    def __str__(self) :
        return f'{self.media_type} id {self.item_id} in {self.playlist.title}'