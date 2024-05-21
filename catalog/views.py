from django.views.generic import ListView

from django.shortcuts import get_object_or_404

from .models import Category, Product


'''
    Класс-представление для страницы каталога категорий
'''
class CatalogView(ListView):
    model = Category
    template_name = 'catalog/catalog.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории товаров'

        return context
    

'''
    Класс-представление для страницы каталога продуктов по категориям
'''
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product-list.html'
    context_object_name = 'products'
    paginate_by = 15

    def get_queryset(self):
        queryset = Product.objects.filter(category__slug=self.kwargs['category_slug'], is_active=True).select_related('category')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог товаров'
        context['selected_category'] = get_object_or_404(Category, slug=self.kwargs['category_slug'])

        return context
    