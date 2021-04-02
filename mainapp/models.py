import sys
from PIL import Image
from io import BytesIO

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse


User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class MinResolutionException(Exception):
    pass


class MaxResolutionException(Exception):
    pass


class LatestProductManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products,
                        key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to),
                        reverse=True
                    )
        return products


class LatestProducts:
    objects = LatestProductManager()


class CategotyManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        "Ноутбуки": "notebook__count",
        "Смартфоны": "smartphone__count",
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('notebook', 'smartphone')
        print(models)
        qs = list(self.get_queryset().annotate(*models).values())
        return [dict(name=c['name'], slug=c['slug'], count=c[self.CATEGORY_NAME_COUNT_NAME[c['name']]]) for c in qs]

class Category(models.Model):

    objects = CategotyManager()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(
        max_length=255,
        verbose_name='Имя категории',
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Номер телефона',
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Адрес'
    )

    def __str__(self):
        return f'Покупатель {self.user.first_name} {self.user.last_name}'


class Product(models.Model):
    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (1000, 1000)
    MAX_SIZE_IMAGE = 2097152

    class Meta:
        abstract = True

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Наименование',
    )
    slug = models.SlugField(
        unique=True,
    )
    image = models.ImageField(
        verbose_name='Изображение',
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
    )
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name='Цена',
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        min_width, min_height = self.MIN_RESOLUTION
        max_width, max_height = self.MAX_RESOLUTION
        if img.width < min_width or img.height < min_height:
            raise MinResolutionException(
                f'Загруженное изображения меньше {self.MIN_RESOLUTION[0]} px x {self.MIN_RESOLUTION[1]} px')
        if img.width > max_width or img.height > max_height:
            converted_img = img.convert('RGB')
            resized_img = converted_img.resize(self.MAX_RESOLUTION, Image.ANTIALIAS)
            imagestream = BytesIO()
            resized_img.save(imagestream, 'JPEG', quality=90)
            self.image = InMemoryUploadedFile(
                imagestream, 'ImageField',
                self.image.name, 'jpeg/image',
                sys.getsizeof(imagestream), None
            )
        super().save(*args, **kwargs)


class Notebook(Product):
    class Meta:
        verbose_name = 'Ноутбук'
        verbose_name_plural = 'Ноутбуки'

    diagonal = models.CharField(
        max_length=255,
        verbose_name='Диагональ'
    )
    display_type = models.CharField(
        max_length=255,
        verbose_name='Тип дисплея'
    )
    processor_freq = models.CharField(
        max_length=255,
        verbose_name='Частота процессора'
    )
    ram = models.CharField(
        max_length=255,
        verbose_name='Оперативная память'
    )
    video = models.CharField(
        max_length=255,
        verbose_name='Видеокарта'
    )
    time_without_charge = models.CharField(
        max_length=255,
        verbose_name='Время работы от аккумулятора'
    )

    def __str__(self):
        return f'{self.category.name} {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Smartphone(Product):
    class Meta:
        verbose_name = 'Смартфон'
        verbose_name_plural = 'Смартфоны'

    diagonal = models.CharField(
        max_length=255,
        verbose_name='Диагональ'
    )
    display_type = models.CharField(
        max_length=255,
        verbose_name='Тип дисплея'
    )
    resolution = models.CharField(
        max_length=255,
        verbose_name='Разрешение экрана'
    )
    accum_volume = models.CharField(
        max_length=255,
        verbose_name='Объем аккумулятора'
    )
    ram = models.CharField(
        max_length=255,
        verbose_name='Оперативная память'
    )
    sd = models.BooleanField(
        default=True,
        verbose_name='Разъем расширения для sd карты'
    )
    sd_volume_max = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Максимальный поддерживаемый объeм SD карты'
    )
    main_cam_mp = models.CharField(
        max_length=255,
        verbose_name='Разрешение главной камеры'
    )
    frontal_cam_mp = models.CharField(
        max_length=255,
        verbose_name='Разрешение фронтальной камеры'
    )

    def __str__(self):
        return f'{self.category.name} {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class CartProduct(models.Model):
    user = models.ForeignKey(
        'Customer',
        verbose_name='Покупатель',
        on_delete=models.CASCADE
    )
    cart = models.ForeignKey(
        'Cart',
        verbose_name='Корзина',
        on_delete=models.CASCADE,
        related_name='related_products'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )
    qty = models.PositiveIntegerField(
        default=1,
        verbose_name='Колличество'
    )
    final_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name='Общая цена',
    )

    def __str__(self):
        return f'Продукт: {self.content_object.title} (для корзины)'


class Cart(models.Model):
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    owner = models.ForeignKey(
        Customer,
        verbose_name='Владелец',
        on_delete=models.CASCADE
    )
    product = models.ManyToManyField(
        CartProduct,
        blank=True,
        related_name='related_cart'
    )
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name='Общая цена',
        default=0,
    )
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}'
