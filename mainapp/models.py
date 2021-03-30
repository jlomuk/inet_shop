from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType


User = get_user_model()


class Category(models.Model):
	
	class Meta:
		verbose_name='Категория'
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
        verbose_name_plural =  'Покупатели'

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
	
	class Meta:
		verbose_name='Продукт'
		verbose_name_plural = 'Продукты'

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
	descriplion = models.TextField(
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


class Notebook(Product):

	class Meta:
		verbose_name='Ноутбук'
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


class Smartphone(Product):

	class Meta:
		verbose_name='Смартфон'
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
		verbose_name='Максимальный объeм встроенной памяти'
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
	product = models.ForeignKey(
		Product,
		verbose_name='Товар',
		on_delete=models.CASCADE,
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
		return f'Продукт: {self.product.title} (для корзины)'


class Cart(models.Model):
	
	class Meta:
		verbose_name='Корзина'
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
	)

	def __str__(self):
		return f'{self.id}'


class Specification(models.Model):
    class Meta:
    	verbose_name = 'Спецификация'
    	verbose_name_plural =  'Спецификации'

    content_type = models.ForeignKey(
    	ContentType,
    	on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    name = models.CharField(
    	max_length=255,
    	verbose_name='Имя товара для характеристик'
    )

    def __str__(self):
    	return f'Характеристики для товара: {self.name}'