from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from django.contrib.sessions import *
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        user = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=user, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')

def sair(request):
    logout(request)
    return redirect('home')