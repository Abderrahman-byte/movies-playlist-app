from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.forms import inlineformset_factory
from django.contrib.auth.models import User

from .forms import CreateUserForm, CreatePlaylistForm
from .models import Playlist
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