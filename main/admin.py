from django.contrib import admin

# Register your models here.
from .models import Profil, Playlist

admin.site.register(Playlist)
admin.site.register(Profil)