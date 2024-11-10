from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as user_logout
from django.http import HttpResponseRedirect





def login(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')

        user = authenticate(request, username=login, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/phone_book/')
        else:
            messages.error(request, 'Невірний логін або пароль.')
    return render(request, 'auth/login.html')


def register(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not all([login, password, password2]):
            messages.error(request, "Всі поля повинні бути заповнені.")
        elif password != password2:
            messages.error(request, "Паролі не співпадають.")
        elif User.objects.filter(username=login).exists():
            messages.error(request, "Користувач з таким логіном вже існує.")
        else:
            user = User.objects.create_user(username=login, password=password)
            auth_login(request, user)
            return redirect('/phone_book/')
    return render(request, 'auth/register.html')


def logout(reguest):
    user_logout(reguest)
    return HttpResponseRedirect("/")