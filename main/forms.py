from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Playlist, Profil

class CreateUserForm(UserCreationForm) :
    class Meta :
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CreatePlaylistForm(forms.ModelForm) :
    class Meta :
        model = Playlist
        fields = ['title']

class ProfilForm(forms.ModelForm) :
    class Meta :
        model = Profil
        fields = '__all__'