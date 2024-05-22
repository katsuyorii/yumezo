from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python

from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from .models import User
from django.contrib.auth import authenticate

from django.contrib.auth.password_validation import validate_password


'''
    Класс для формы авторизации пользователей
'''
class LoginUserForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'login-email-input', 
        'placeholder': 'Введите email',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs= {
        'class': 'login-email-input', 
        'placeholder': 'Введите пароль',
    }))

    # Метод валидации формы
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = authenticate(username=email, password=password)
        if user is None:
            raise forms.ValidationError('Неправильный email или пароль.')
        
        self.cleaned_data['user'] = user
        return self.cleaned_data

