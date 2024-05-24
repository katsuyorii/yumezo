from django.urls import path
from .views import LoginUserView, RegistrationUserView, ProfileUserView, LogoutUserView, ChangePasswordUserView, EditInfoUserView

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('registration/', RegistrationUserView.as_view(), name='registration'),
    path('profile/', login_required(ProfileUserView.as_view()), name='profile'),
    path('logout/', login_required(LogoutUserView.as_view()), name='logout'),
    path('change-password/', login_required(ChangePasswordUserView.as_view()), name='change_password'),
    path('profile-edit/', login_required(EditInfoUserView.as_view()), name='profile_edit'),
]