from django.db import models


'''
    Модель изображения для слайдера на главной странице сайта.
'''
class SliderImage(models.Model):
    image_slider = models.ImageField(verbose_name='Изображение', upload_to='images_slider')

    class Meta:
        verbose_name = 'Изображение слайдера'
        verbose_name_plural = 'Изображения слайдеров'
        
    # При удалении объекта удаляется связанное фото из папки media
    def delete(self, *args, **kwargs):
        self.image_slider.delete()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.image_slider.url
    

'''
    Модель изображения для новостного продукта на главной странице сайта.
'''
class NewsProductImage(models.Model):
    image_news_product = models.ImageField(verbose_name='Изображение', upload_to='images_news_products')

    class Meta:
        verbose_name = 'Изображение новостного продукта'
        verbose_name_plural = 'Изображения новостного продукта'

    # Перед сохранением нового объекта, делается выборка, которая не соответсвует PK нового изображения и удаляется.
    def save(self, *args, **kwargs):
        NewsProductImage.objects.exclude(pk=self.pk).delete()
        super().save(*args, **kwargs)

    # При удалении объекта удаляется связанное фото из папки media
    def delete(self, *args, **kwargs):
        self.image_news_product.delete()
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return self.image_news_product.url