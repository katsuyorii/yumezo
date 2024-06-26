from django.urls import path
from .views import LoginUserView, RegistrationUserView, ProfileUserView, LogoutUserView, ChangePasswordUserView, EditInfoUserView, ActivateEmailDoneView, ActivateEmailCheckView, ActivateEmailConfirmView, ActivateEmailErrorView, ActivateEmailRepeatSendView, FavoritesUserView, FavoritesDeleteUserView, ForgotPasswordChangeView, ForgotPasswordEmailCheckView, ForgotPasswordEmailView, CartUserView, CartAddView, CartDeleteView, CartClearView, OrdersUserView, CartChangeView

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('registration/', RegistrationUserView.as_view(), name='registration'),
    path('profile/', login_required(ProfileUserView.as_view()), name='profile'),
    path('logout/', login_required(LogoutUserView.as_view()), name='logout'),
    path('change-password/', login_required(ChangePasswordUserView.as_view()), name='change_password'),
    path('profile-edit/', login_required(EditInfoUserView.as_view()), name='profile_edit'),

    path('cart/', login_required(CartUserView.as_view()), name='cart'),
    path('cart_change/', login_required(CartChangeView.as_view()), name='cart_change'),
    path('cart-add/<int:product_id>', login_required(CartAddView.as_view()), name='cart_add'),
    path('cart-delete/<int:cart_id>', login_required(CartDeleteView.as_view()), name='cart_delete'),
    path('cart-clear/', login_required(CartClearView.as_view()), name='cart_clear'),

    path('favorites/', login_required(FavoritesUserView.as_view()), name='favorites'),
    path('delete-favorites/<int:favorites_id>', login_required(FavoritesDeleteUserView.as_view()), name='delete_favorites'),

    path('orders/', login_required(OrdersUserView.as_view()), name='orders'),

    path('activate-email-done/', login_required(ActivateEmailDoneView.as_view()), name='activate_email_done'),
    path('activate-email-check/<uidb64>/<token>/', login_required(ActivateEmailCheckView.as_view()), name='activate_email_check'),
    path('activate-email-confirm/', login_required(ActivateEmailConfirmView.as_view()), name='activate_email_confirm'),
    path('activate-email-not-confirm/', login_required(ActivateEmailErrorView.as_view()), name='activate_email_not_confirm'),
    path('activate-email-repeat/', login_required(ActivateEmailRepeatSendView.as_view()), name='activate_email_repeat'),

    path('forgot-password-email/', ForgotPasswordEmailView.as_view(), name='forgot_password_email'),
    path('forgot-password-change/<uidb64>/', ForgotPasswordChangeView.as_view(), name='forgot_password_change'),
    path('forgot-password-email-check/<uidb64>/<token>/', ForgotPasswordEmailCheckView.as_view(), name='forgot_password_email_check'),
]