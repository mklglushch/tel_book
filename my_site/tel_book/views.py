from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from .models import Contact
from django.contrib.auth import authenticate, login as auth_login, logout as user_logout
from django.contrib.auth.models import User
from .forms import ContactForm
from django.contrib import messages


def home_page(request):
    return render(request, 'contacts/home_page.html')


#list contacts
def show_phone_book(request):
    phones = Contact.objects.all()
    return render(request, 'phone_numbers/phone book.html', {'phones': phones})


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


#logout
def logout(reguest):
    user_logout(reguest)
    return HttpResponseRedirect("/")




#list contacts for edit
def edit_contact(request, id):
    try:
        if request.user.is_superuser:
            contact = get_object_or_404(Contact, id=id)
        else:
            contact = get_object_or_404(Contact, id=id, user=request.user)
    except:
        messages.error(request, "Ви не можете редагувати цей контакт, оскільки він вам не належить.")
        return redirect(show_phone_book)

    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, "Контакт успішно оновлено.")
            return redirect(show_phone_book) 
    else:
        form = ContactForm(instance=contact)
    return render(request, 'edit_contact.html', {'form': form})


# delete contact
def delete_contact(request, id):
    if not request.user.is_superuser:
        return redirect(show_phone_book)
    contact = get_object_or_404(Contact, id=id)
    if request.method == 'POST':
        contact.delete()
        return redirect(show_phone_book)
    return render(request, 'confirm_delete.html', {'contact': contact})


# add contact
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            UserProfile = form.save(commit=False)
            UserProfile.user = request.user 
            UserProfile.save()
            form.save()
            return redirect(show_phone_book)
    else:
        form = ContactForm()
    return render(request, 'add_contact.html', {'form': form})