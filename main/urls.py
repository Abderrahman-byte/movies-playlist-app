from django.urls import path

from . import views

# app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegiterView.as_view(), name='register'),
    path('logout/', views.logoutView, name='logout'),

    path('trending/', views.TrendingView, name='trending'),
    path('playlists/', views.playlistsView, name='playlists'),
    path('playlists/add/', views.CreatePlaylistView, name='create_playlist'),
    path('playlists/<uuid:id>/edit/', views.EditPlaylistView, name='edit_playlist'),

    path('details/<str:media_type>/<int:id>/', views.mediaDetailsView, name='media_details')
]