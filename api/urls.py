from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('trending/', views.trendingApi, name='trending'),
    path('playlists/', views.playlistsApi, name='playlists')
]