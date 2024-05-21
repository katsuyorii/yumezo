from django.views.generic import TemplateView, ListView
from .models import SliderImage, NewsProductImage
from catalog.models import Product

'''
    Класс-представление для страницы - "Главная".
'''
class IndexView(ListView):
    model = Product
    template_name = 'core/index.html'
    context_object_name = 'hits'

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).order_by('-count_sales')[:5].select_related('category')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Аниме магазин Yumezo'
        context['slider_images'] = SliderImage.objects.all()
        context['news_product_images'] = NewsProductImage.objects.first()
        context['manga_list'] = Product.objects.filter(category__slug='manga', is_active=True)[:5].select_related('category')

        return context


'''
    Класс-представление для страницы - "О нас".
'''
class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О нас'

        return context
    

'''
    Класс-представление для страницы - "Оплата и доставка".
'''
class DeliveryView(TemplateView):
    template_name = 'core/delivery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оплата и доставка'

        return context
    

'''
    Класс-представление для страницы - "Возврат и обмен".
'''
class RefundView(TemplateView):
    template_name = 'core/refund.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Возврат и обмен'

        return context
    

'''
    Класс-представление для страницы - "Контакты".
'''
class ContactsView(TemplateView):
    template_name = 'core/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'

        return context
