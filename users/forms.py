from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python

from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from .models import User
from catalog.models import Order
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


'''
    Класс для формы смены пароля
'''
class ChangePasswordUserForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login-email-input',
    }))

    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login-email-input',
    }))

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login-email-input',
    }))


'''
    Класс для формы редактирования профиля
'''
class EditInfoUserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'login-email-input', 
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'login-email-input', 
    }), help_text='При изменении адреса электронной почты, новую почту необходимо будет подтвердить, перейдя по ссылке из пиcьма, которое будет отправлено на текущий адрес. До подтверждения аккаунт будет неактивен.')

    phone_number = PhoneNumberField(required=False, widget=forms.TextInput(attrs={
        'class': 'login-email-input', 
    }))

    profile_image = forms.ImageField(required=False, widget=forms.FileInput(), help_text='Файл изображения размером не более 100MB')

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'profile_image']
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        return to_python(phone_number)
    

'''
    Класс для формы восстановления пароля
'''
class ForgotPasswordEmailForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'login-email-input', 
        'placeholder': 'Введите email',
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email не найден!')
        
        return email


'''
    Класс для формы изменения пароля у пользователя после восстановления
'''
class ForgotPasswordChangeForm(forms.Form):
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
    

'''
    Класс для формы оформления заказа
'''
class OrderForm(forms.ModelForm):
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'cart-contacts-info-row-item-input', 
        'placeholder': 'Введите населенный пункт',
    }))

    street = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'cart-contacts-info-row-item-input', 
        'placeholder': 'Введите улицу',
    }))

    house = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'cart-contacts-info-row-item-input', 
        'placeholder': 'Введите дом или корпус',
    }))

    apart = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'cart-contacts-info-row-item-input', 
        'placeholder': 'Введите квартиру',
    }))

    postcode = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'cart-contacts-info-row-item-input', 
        'placeholder': 'Введите почтовый индекс',
    }))

    comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'cart-contacts-info-comment', 
        'placeholder': 'Введите комментарий к заказу...',
    }))

    class Meta:
        model = Order
        fields = ['city', 'street', 'house', 'apart', 'postcode', 'comment']