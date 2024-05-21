from django.db import models
from pytils.translit import slugify


'''
    Модель описывающая категории товаров (прим. "Манга", "Одежда и аксессуары", "Фигурки")
'''
class Category(models.Model):
    name = models.CharField(verbose_name='Наименование категории', max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True, db_index=True, editable=False)
    image = models.ImageField(verbose_name='Изображение категории', upload_to='icons_categories')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    '''
        Переопределение метода сохранения записи.
        С помощью библиотеки pytils переводим киррилицу в латиницу по полю name.
        В поле slug записывается поле name на латинице.
    '''
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

'''
    Модель описывающая жанры товаров (прим. "Боевик", "Драма", "Фэнтези")
'''
class Genre(models.Model):
    name = models.CharField(verbose_name='Наименование жанра', max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True, db_index=True, editable=False)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    '''
        Переопределение метода сохранения записи.
        С помощью библиотеки pytils переводим киррилицу в латиницу по полю name.
        В поле slug записывается поле name на латинице.
    '''
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

'''
    Модель описывающая источник товаров (прим. "Naruto", "Bleach", "Death Note")
'''
class Source(models.Model):
    name = models.CharField(verbose_name='Наименование источника', max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True, db_index=True, editable=False)

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'

    '''
        Переопределение метода сохранения записи.
        С помощью библиотеки pytils переводим киррилицу в латиницу по полю name.
        В поле slug записывается поле name на латинице.
    '''
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

'''
    Модель описывающая базовые характеристики товаров, которые встречаются у всех (прим. "Наименование", "Источник", "Цена")
'''
class Product(models.Model):
    name = models.CharField(verbose_name='Наименование товара', max_length=128)
    name_eng = models.CharField(verbose_name='Наименование товара (англ.)', max_length=128)
    slug = models.SlugField(max_length=128, unique=True, db_index=True, editable=False)
    category = models.ForeignKey(verbose_name='Категория', to=Category, on_delete=models.CASCADE)
    source = models.ForeignKey(verbose_name='Источник', to=Source, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Изображение продукта', upload_to='icons_products')
    description = models.TextField(verbose_name='Описание товара')
    price = models.PositiveIntegerField(verbose_name='Цена', help_text='Цена указывается в рублях (руб.)')
    discount = models.PositiveIntegerField(verbose_name='Скидка', default=0, help_text='Скидка указывается в процентах (%)')
    amount = models.PositiveIntegerField(verbose_name='Количество в наличии', default=0)
    is_active = models.BooleanField(verbose_name='Активный продукт', default=False)
    count_sales = models.PositiveIntegerField(verbose_name='Количество продаж', default=0, editable=False)
    rating = models.SmallIntegerField(verbose_name='Средний рейтинг товара', default=0, editable=False)

    class Meta:
        verbose_name = 'Базовый продукт'
        verbose_name_plural = 'Базовые продукты'

    '''
        Переопределение метода сохранения записи.
        С помощью библиотеки pytils переводим киррилицу в латиницу по полю name.
        Авто-слаг, при добавлении в конец слага добавляется id.
    '''
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name) + '-' + str(self.pk)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    # Метод преобразования цены с учетом скидки, если она есть
    def price_discount(self):
        if self.discount:
            return int(self.price + ((self.price * self.discount) / 100))
        
        return self.price
    

'''
    Модель описывающая специфические для разных категорий характеристики товаров (прим. "Вес", "Размер", "Длина")
'''
class Property(models.Model):
    name = models.CharField(verbose_name='Наименование характеристики', max_length=128)

    class Meta:
        verbose_name = 'Характеристика продукта'
        verbose_name_plural = 'Характеристики продуктов'

    def __str__(self):
        return self.name
    

'''
    Модель описывающая значение для спец. характеристики продукта (прим. "Вес - 100 гр.", "Размер - XL", "Длина - 20 см.")
'''
class ProductProperty(models.Model):
    product = models.ForeignKey(verbose_name='Продукт', to=Product, on_delete=models.CASCADE)
    property = models.ForeignKey(verbose_name='Характеристика', to=Property, on_delete=models.CASCADE)
    value_string = models.CharField(verbose_name='Текстовое значение характеристики', max_length=250, null=True, blank=True, help_text='Значение задается текстом')
    value_integer = models.IntegerField(verbose_name='Числовое значение характеристики', null=True, blank=True, help_text='Значение задается целым числом')
    value_genres = models.ManyToManyField(verbose_name='Жанры', to=Genre, null=True, blank=True, help_text='Поле для категорий, в которых есть поле - жанры')

    class Meta:
        verbose_name = 'Сопоставление характеристик продуктов'
        verbose_name_plural = 'Сопоставление характеристик продуктов'

    def __str__(self):
        return f'{self.product.name} | {self.property.name}'