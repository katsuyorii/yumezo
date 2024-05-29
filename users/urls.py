from django.urls import path
from .views import LoginUserView, RegistrationUserView, ProfileUserView, LogoutUserView, ChangePasswordUserView, EditInfoUserView, ActivateEmailDoneView, ActivateEmailCheckView, ActivateEmailConfirmView, ActivateEmailErrorView, ActivateEmailRepeatSendView, FavoritesUserView, FavoritesDeleteUserView, ForgotPasswordChangeView, ForgotPasswordEmailCheckView, ForgotPasswordEmailView

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('registration/', RegistrationUserView.as_view(), name='registration'),
    path('profile/', login_required(ProfileUserView.as_view()), name='profile'),
    path('logout/', login_required(LogoutUserView.as_view()), name='logout'),
    path('change-password/', login_required(ChangePasswordUserView.as_view()), name='change_password'),
    path('profile-edit/', login_required(EditInfoUserView.as_view()), name='profile_edit'),

    path('favorites/', login_required(FavoritesUserView.as_view()), name='favorites'),
    path('delete-favorites/<int:favorites_id>', login_required(FavoritesDeleteUserView.as_view()), name='delete_favorites'),

    path('activate-email-done/', login_required(ActivateEmailDoneView.as_view()), name='activate_email_done'),
    path('activate-email-check/<uidb64>/<token>/', login_required(ActivateEmailCheckView.as_view()), name='activate_email_check'),
    path('activate-email-confirm/', login_required(ActivateEmailConfirmView.as_view()), name='activate_email_confirm'),
    path('activate-email-not-confirm/', login_required(ActivateEmailErrorView.as_view()), name='activate_email_not_confirm'),
    path('activate-email-repeat/', login_required(ActivateEmailRepeatSendView.as_view()), name='activate_email_repeat'),

    path('forgot-password-email/', ForgotPasswordEmailView.as_view(), name='forgot_password_email'),
    path('forgot-password-change/<uidb64>/', ForgotPasswordChangeView.as_view(), name='forgot_password_change'),
    path('forgot-password-email-check/<uidb64>/<token>/', ForgotPasswordEmailCheckView.as_view(), name='forgot_password_email_check'),
]