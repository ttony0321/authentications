from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import RegisterForm, LoginForm
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


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        self.request.session['user'] = form.data.get('email')
        return super().form_valid(form)


def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('/')

