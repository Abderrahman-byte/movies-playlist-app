from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('trending/', views.trendingApi, name='trending'),
    path('playlists/', views.playlistsApi, name='playlists'),
    path('playlists_lite/', views.PlaylistLiteView, name='playlists_lite'),
    path('playlists/<uuid:id>/delete/', views.deletePlaylist, name='delete_playlist'),
    path('playlist/<uuid:id>/', views.deleteItemFromPlaylist, name='delete_form_playlist'),
    path('playlist/add/<uuid:id>/', views.addToPlaylistView , name='add_to_playlist')
]