from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Contact
from django import forms



class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логін', max_length=254)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'surname', 'father_name', 'type_contact', 'phone', 'email']


