from django.urls import path
from .views import CatalogView, ProductListView


urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('<slug:category_slug>/', ProductListView.as_view(), name='product_list'),
]