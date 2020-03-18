from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate

from .forms import CreateUserForm
# Create your views here.

# HOME VIEW FUNCTION BASE
def index(request) :
    return render(request, 'main/index.html')

# LOGIN VIEW CLASS BASE
class LoginView(View) :
    def get(self, request) :
        return render(request, 'main/login.html')

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
def logout(request) :
    return HttpResponse('<h1>Logged out</h1>')