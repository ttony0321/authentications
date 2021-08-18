from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from django.contrib.auth import get_user_model
User = get_user_model()
from django.views.generic import FormView

# Create your views here.


def index(request):
    return render(request, 'users/index.html')


def register(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                email=request.POST['email'], username=request.POST['username'], password=request.POST['password1']
            )
            auth.login(request, user)
            return redirect('/users/index/')
        return render(request, 'users/register.html')
    return render(request, 'users/register.html')


def loginuser(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'users/login.html', {'error' : 'username or password is incorrect.'})
    else:
        return render(request, 'users/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')


def profile(request):
    user = request.user
    return render(request, 'users/profile.html', {'user': user})