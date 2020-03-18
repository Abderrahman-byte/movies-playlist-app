from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegiterView.as_view(), name='register'),
    path('logout/', views.logoutView, name='logout')
]