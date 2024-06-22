from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from users.models import User
from django.db.models import Avg


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

    def get_absolute_url(self):
        return reverse('product_list', kwargs={"category_slug": self.slug})

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
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={"category_slug": self.category.slug, "product_slug": self.slug})
    
    # Метод преобразования цены с учетом скидки, если она есть
    def price_discount(self):
        if self.discount:
            return int(self.price + ((self.price * self.discount) / 100))
        
        return self.price
    

    # Метод рассчета рейтинга
    def update_rating(self):
        average_grade = Comment.objects.filter(product__slug=self.slug).aggregate(avg_grade=Avg('grade'))['avg_grade']
        
        if average_grade is None:
            self.rating = 0
        else:
            self.rating = average_grade
            
        self.save()

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
    

'''
    Модель описывающая комментарии пользователей
'''
class Comment(models.Model):
    product = models.ForeignKey(verbose_name='Продукт', to=Product, on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE)
    review_text = models.TextField(verbose_name='Текст комментария')
    create_date = models.DateTimeField(verbose_name='Дата создания комментария', auto_now_add=True)
    grade = models.SmallIntegerField(verbose_name='Оценка пользователя')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.product.name} | {self.user.username}'
    

'''
    Модель описывающая избранное пользователей
'''
class Favorites(models.Model):
    product = models.ForeignKey(verbose_name='Продукт', to=Product, on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} | {self.product.name}'

    def get_absolute_url(self):
        return reverse('delete_favorites', kwargs={"favorites_id": self.pk})

    class Meta:
        verbose_name = 'Избранное пользователя'
        verbose_name_plural = 'Избранное пользователей'


'''
    Модель описывающая корзину пользователя
'''
class Cart(models.Model):
    product = models.ForeignKey(verbose_name='Продукт', to=Product, on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name='Количество', default=1)

    def __str__(self):
        return f'{self.user.username} | {self.product.name} | {self.amount}'
    
    def total_price_not_sale(self):
        return self.amount * self.product.price
    
    def total_price_sale(self):
        return self.amount * self.product.price_discount()

    class Meta:
        verbose_name = 'Корзина пользователя'
        verbose_name_plural = 'Корзины пользователей'


'''
    Модель описывающая заказ пользователя
'''
class Order(models.Model):
    class Status(models.TextChoices):
        CR = 'CR', 'Создан'
        DEL = 'DEL', 'В доставке'
        CONF_DEL = 'CONF_DEL', 'Доставлен'
        REC = 'REC', 'Получен'

    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE)
    products = models.ManyToManyField(verbose_name='Продукты для заказа', to=Product)
    city = models.CharField(verbose_name='Город / Населенный пункт', max_length=255)
    street = models.CharField(verbose_name='Улица', max_length=255)
    house = models.PositiveSmallIntegerField(verbose_name='Дом / корпус')
    apart = models.PositiveSmallIntegerField(verbose_name='Квартира')
    postcode = models.IntegerField(verbose_name='Почтовый индекс')
    create_date = models.DateField(auto_now_add=True, db_index=True)
    total_price = models.PositiveIntegerField('Общая стоимость заказа', default=0)
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    status = models.CharField(verbose_name='Статус заказа', choices=Status.choices, default=Status.CR)

    def __str__(self):
        return f'{self.user.username} | {self.user.username} | {self.create_date} | {self.total_price}'
    
    class Meta:
        verbose_name = 'Заказ пользователя'
        verbose_name_plural = 'Заказы пользователей'