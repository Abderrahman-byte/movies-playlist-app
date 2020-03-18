from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.
def index(request) :
    return render(request, 'main/index.html')

class LoginView(View) :
    def get(self, request) :
        return HttpResponse('<h1>login</h1>')

class RegiterView(View) :
    def get(self, request) :
        return HttpResponse('<h1>Register</h1>') 

def logout(request) :
    return HttpResponse('<h1>Logged out</h1>')