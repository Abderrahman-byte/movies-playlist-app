from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.urls import reverse
from django.contrib import messages

from .forms import CreateUserForm
# Create your views here.

# HOME VIEW FUNCTION BASE
def index(request) :
    return render(request, 'main/index.html')

# LOGIN VIEW CLASS BASE
class LoginView(View) :
    def get(self, request) :
        return HttpResponse('<h1>login</h1>')

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

            return redirect(reverse('login'))
        
        else :
            for error in form.error_messages :
                messages.error(request, form.error_messages.get(error))

            return render(request, 'main/register.html', { 'form': form })

# LOGOUT VIEW CLASS BASE
def logout(request) :
    return HttpResponse('<h1>Logged out</h1>')