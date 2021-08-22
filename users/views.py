from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout as quick_logout
from .forms import RegisterForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from .models import User as usertest
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
            return redirect('users:profile')
        return render(request, 'users/register.html')
    return render(request, 'users/register.html')


def loginuser(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('users:profile')
        else:
            return render(request, 'users/login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'users/login.html')


def logout(request):
    quick_logout(request)
    return redirect('users:login')


def profile(request):
    user = request.user

    return render(request, 'users/profile.html', {'user': user})

#@require_http_methods(['GET', 'POST'])
@login_required
def update(request):
    if not request.user.is_authenticated:
        return redirect('users:index')
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    context = {'form': form}
    return render(request, 'users/profile_edit.html', context)


#password

