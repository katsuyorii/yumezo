from django.urls import path
from .views import LoginUserView, RegistrationUserView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('registration/', RegistrationUserView.as_view(), name='registration'),
]