from django.http import HttpResponseRedirect

from django.urls import reverse_lazy

from django.db import transaction

from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from django.shortcuts import get_object_or_404

from .models import Category, Product, ProductProperty, Comment
from .forms import AddNewCommentForm

from django.contrib.auth.models import AnonymousUser


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
    

'''
    Класс-представление для страницы отдельного товара
'''
class ProductDetailView(DetailView, FormMixin):
    model = Product
    form_class = AddNewCommentForm
    template_name = 'catalog/product-detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_queryset(self):
        queryset = Product.objects.filter(slug=self.kwargs['product_slug']).select_related('category', 'source')

        return queryset

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['title'] = self.object.name
        context['proretries'] = ProductProperty.objects.filter(product__slug=self.kwargs['product_slug']).select_related('property')
        context['comments'] = Comment.objects.filter(product__slug=self.kwargs['product_slug']).select_related('user').order_by('-create_date')
        context['count_reviews'] = Comment.objects.filter(product__slug = self.kwargs['product_slug']).count()

        # Проверка, если пользователь не авторизирован, то у него нет доступа к форме создания комментария и добавления в избранное
        if isinstance(self.request.user, AnonymousUser):
            context['is_user_comment'] = True
        else:
            context['is_user_comment'] = Comment.objects.filter(user=self.request.user, product__slug=self.kwargs['product_slug']).exists()

        return context
    
    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs = {'category_slug': self.kwargs['category_slug'], 'product_slug': self.kwargs['product_slug']})
    
    # Метод добавления комментариев
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
            new_comment.user = self.request.user
            new_comment.save()
            new_comment.product.update_rating()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_success_url())
    