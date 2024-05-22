from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import get_user_model

# Кастомная бэкенд аутентификация по Email
class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_moel = get_user_model()
        try:
            user = user_moel.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (user_moel.DoesNotExist, user_moel.MultipleObjectsReturned):
            return None
        
    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
