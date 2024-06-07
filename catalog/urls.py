from django.urls import path

from .views import CatalogView, ProductListView, ProductDetailView, CommentDeleteView, CommentEditView, FavoritesAddUserView, SearchProductListView, DynamicFiltersProducts

from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('search/', SearchProductListView.as_view(), name='search'),
    path('<slug:category_slug>/', ProductListView.as_view(), name='product_list'),
    path('<slug:category_slug>/<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),

    path('delete_comment/<int:comment_id>', CommentDeleteView.as_view(), name='delete_comment'),
    path('edit_comment/<int:comment_id>', CommentEditView.as_view(), name='edit_comment'),

    path('add_favorites/<int:product_id>', login_required(FavoritesAddUserView.as_view()), name='add_favorites'),

    path('dynamic-filters/', DynamicFiltersProducts.as_view(), name='dynamic-filters'),
]