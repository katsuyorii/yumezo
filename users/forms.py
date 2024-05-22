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


'''
    Класс для формы регистрации новых пользователей
'''
class RegistrationUserForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'login-email-input', 
        'placeholder': 'Введите email',
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'login-email-input', 
        'placeholder': 'Введите имя пользователя',
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs= {
        'class': 'login-email-input', 
        'placeholder': 'Введите пароль',
    }), validators=[validate_password])
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs= {
        'class': 'login-email-input', 
        'placeholder': 'Введите пароль',
    }), validators=[validate_password])
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Введенные пароли отличаются!')
        
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует!')
        
        return email
