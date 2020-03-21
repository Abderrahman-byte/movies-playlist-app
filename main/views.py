from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.conf import settings

import requests as fetcher
import json

from .forms import CreateUserForm, CreatePlaylistForm, ProfilForm
from .models import Playlist, Profil
# Create your views here.

# HOME VIEW FUNCTION BASE
def index(request) :
    return render(request, 'main/index.html')

# LOGIN VIEW CLASS BASE
class LoginView(View) :
    def get(self, request) :
        next = request.GET.get('next')
        return render(request, 'main/login.html', { 'next': next })

    def post(self, request) :
        next = request.POST.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None :
            login(request, user)

            if next is not None :
                return redirect(next)
            else :
                return redirect(reverse('home'))
        
        else :
            messages.error(request, 'username or password is not correct')
            return redirect(reverse('login'))


# REGISTER VIEW CLASS BASE
class RegiterView(View) :
    def get(self, request) :
        form = CreateUserForm()

        context = { 'form': form }
        return render(request, 'main/register.html', context)

    def post(self, request) :
        form = CreateUserForm(request.POST)

        if form.is_valid() :
            user = form.save()
            username = user.username

            messages.success(request, f'user created {username} successfully')
            return redirect(reverse('login'))

        else :
            for error in form.error_messages :
                messages.error(request, form.error_messages.get(error))

            return render(request, 'main/register.html', { 'form': form })

# LOGOUT VIEW CLASS BASE
def logoutView(request) :
    logout(request)
    return redirect(reverse('home'))

# Trending VIEW FUNCTION BASE
def TrendingView(request) :
    return render(request, 'main/trending.html')

# Playlists VIEW FUNCTION BASE
def playlistsView(request) :
    return render(request, 'main/playlists.html')

def CreatePlaylistView(request) :
    if request.method == 'GET' :
        form = CreatePlaylistForm()
        return render(request, 'main/create_playlist.html', {'form': form})

    if request.method == 'POST' :
        form = CreatePlaylistForm(request.POST)
        user = request.user
        
        if user.playlist_set.all().count() >= 5 :
            messages.error(request, 'You Cannot Have More Than 5 Playlists.')
            return render(request, 'main/create_playlist.html', {'form': form}) 
        
        try :
            Playlist(title=request.POST['title'], creator=user).save()
            return redirect(reverse('playlists'))
        except Exception as ex :
            messages.error(request, ex)
            return render(request, 'main/create_playlist.html', {'form': form}) 

def EditPlaylistView(request, id) :
    if request.method == 'GET' :
        playlist = Playlist.objects.get(pk=id)
        form = CreatePlaylistForm(instance=playlist)
        
        return render(request, 'main/edit_playlist.html', { 'form': form })

    if request.method == 'POST' :
        playlist = Playlist.objects.get(pk=id)
        form = CreatePlaylistForm(request.POST, instance=playlist, initial={ 'user': request.user })

        try :
            form.save()
            return redirect(reverse('playlists'))
        except Exception as ex :
            messages.error(request, ex)
            return render(request, 'main/create_playlist.html', {'form': form})

def mediaDetailsView(request, media_type, id) :
    api_key = settings.TMDB_API_KEY
    url = f'https://api.themoviedb.org/3/{media_type}/{id}?api_key={api_key}'
    
    req = fetcher.get(url)
    details = json.loads(req.text)

    if req.status_code == 200 :
        context = {'media': {'media_type': media_type, **details} }
        return render(request, 'main/details.html', context)
    else :
        return render(request, 'main/Notfound.html')

def handle_uploaded_file(f):
    with open('C:/Users/ENVY/Desktop/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def profilView(request) :
    user = Profil.objects.get(user=request.user)
    form = ProfilForm(instance=user)
    
    if request.method == 'POST' :
        form = ProfilForm(request.POST, request.FILES, instance=user)

        if form.is_valid() :
            form.save()
            return redirect(reverse('profil'))
        else :
            for error in form.errors :
                messages.error(request, form.errors.get(error))

    return render(request, 'main/profil.html', { 'form': form })