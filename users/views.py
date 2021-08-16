from django.shortcuts import render
from .forms import RegisterForm
# Create your views here.


def register(request):
    if request.method == 'POST':        #POST 면 전달받은 FORM의 유효성을 검사하고 db저장
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            return render(request, 'users/login.html', {'user': user})

    elif request.method == 'GET':       #get이면 그냥 FORM을 띄워준다.
        user_form = RegisterForm()
        return render(request, 'users/register.html', {'user_form': user_form})
