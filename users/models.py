from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


'''
    Переопредление модели User, добавление номера телефона, аватара профиля, email. Замена основого поля с username email.
'''
class User(AbstractUser):
    email = models.EmailField(verbose_name='Email', unique=True)
    username = models.CharField('Имя пользователя', max_length=100)
    profile_image = models.ImageField(verbose_name='Изображение профиля', upload_to='users_profile_images', null=True, blank=True)
    phone_number = PhoneNumberField(verbose_name='Номер телефона', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email