from django.contrib import admin

# Register your models here.
from .models import Profil, Playlist, PlaylistItem

admin.site.register(Playlist)
admin.site.register(Profil)
admin.site.register(PlaylistItem)