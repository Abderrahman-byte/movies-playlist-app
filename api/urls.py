from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('trending/', views.trendingApi, name='trending')
]