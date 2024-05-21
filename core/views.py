from django.views.generic import TemplateView
from .models import SliderImage, NewsProductImage


class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Аниме магазин Yumezo'
        context['slider_images'] = SliderImage.objects.all()
        context['news_product_images'] = NewsProductImage.objects.first()
