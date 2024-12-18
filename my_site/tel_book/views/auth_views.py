from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as user_logout
from django.http import HttpResponseRedirect




def login(request):
    has_error = False
    error_message = ""
    
    if request.method == 'POST':
        login_input = request.POST.get('login')
        password = request.POST.get('password')

        user = authenticate(request, username=login_input, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/phone_book/')
        else:
            has_error = True
            error_message = "Невірний логін або пароль"
    
    return render(request, 'auth/login.html', {
        'has_error': has_error,
        'error_message': error_message
    })




def register(request):
    has_error = False
    error_message = ""

    if request.method == 'POST':
        login_input = request.POST.get('login')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Логіка перевірки введених даних
        if not all([login_input, password, password2]):
            has_error = True
            error_message = "Всі поля повинні бути заповнені."
        elif password != password2:
            has_error = True
            error_message = "Паролі не співпадають."
        elif User.objects.filter(username=login_input).exists():
            has_error = True
            error_message = "Користувач вже існує."
        else:
            # Створення користувача та перенаправлення
            user = User.objects.create_user(username=login_input, password=password)
            auth_login(request, user)
            return redirect('/phone_book/')
    
    # Передача контексту в шаблон
    return render(request, 'auth/register.html', {
        'has_error': has_error,
        'error_message': error_message
    })




def logout(reguest):
    user_logout(reguest)
    return HttpResponseRedirect("/")