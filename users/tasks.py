from .models import User
from .services import SendEmail

from celery import shared_task

# Функция отправки email, которая будет использоваться в Celery
@shared_task
def activate_email_task(user_pk):  
    user = User.objects.get(pk=user_pk)
    send_email = SendEmail(user=user)  
    send_email.send_activate_email()


# Функция отправки email для восстановления пароля, которая будет использоваться в Celery
@shared_task
def forgot_password_email_task(user_pk): 
    user = User.objects.get(pk=user_pk) 
    send_email = SendEmail(user=user)  
    send_email.send_forgot_password_email()