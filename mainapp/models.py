from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse


User = get_user_model()


class Category(models.Model):

    name = models.CharField(max_length=255,verbose_name='Имя категории',)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'    

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Customer(models.Model):
 
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_customer')

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return f'Покупатель {self.user} {self.user.first_name} {self.user.last_name}'


class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__._meta.model_name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})



class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1, verbose_name='Кол-во')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена итого')

    def __str__(self):
        return f'Продукт: {self.product.title} (для корзины)'

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey(Customer, verbose_name='Владелец', on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField( CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0, null=True, blank=True)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена', default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Kорзина № {self.id} для покупателя'


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY,'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен'),
    )

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    BUYING_TYPE_CHOISES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка'),
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель',related_name="related_orders", on_delete=models.CASCADE,)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name =  models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True )
    address = models.CharField(max_length=255, verbose_name='Адрес') 
    status = models.CharField(max_length=100, verbose_name='Статус заказа', choices=STATUS_CHOICES,default=STATUS_NEW)
    buying_type = models.CharField(max_length=100, verbose_name='Тип доставки', choices=BUYING_TYPE_CHOISES, default=BUYING_TYPE_SELF)
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ № {self.id}_покупатель {self.customer.user}'