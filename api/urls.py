from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('trending/', views.trendingApi, name='trending'),
    path('playlists/', views.playlistsApi, name='playlists'),
    path('playlist/<uuid:id>/', views.deleteItemFromPlaylist.as_view(), name='delete_form_playlist')
]