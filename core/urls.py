from django.urls import path
from .views import IndexView, AboutView, DeliveryView, RefundView, ContactsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('delivery/', DeliveryView.as_view(), name='delivery'),
    path('refund/', RefundView.as_view(), name='refund'),
    path('about/', AboutView.as_view(), name='about'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]

