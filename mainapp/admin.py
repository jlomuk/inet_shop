from PIL import Image
from django.contrib import admin 
from django.forms import ModelForm, ValidationError
from django.utils.safestring import mark_safe

from . import models


class ImageValidationAdminForm(ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['image'].help_text = mark_safe('<span style="color:red; font-size:12px;">\
			Загружайте изображение в пределах от {}x{} px до {}x{} px и размером не более 2 мб</span>'.format(\
				*models.Product.MIN_RESOLUTION, *models.Product.MAX_RESOLUTION
			)
		)

	def clean_image(self):
		image = self.cleaned_data.get('image')
		img = Image.open(image)
		min_width, min_height = models.Product.MIN_RESOLUTION
		max_width, max_height = models.Product.MAX_RESOLUTION
		if image.size > models.Product.MAX_SIZE_IMAGE:
			raise ValidationError('Загруженное изображение превышает максимальное значение в 2 мб')
		if img.width < min_width or img.height < min_height:
			raise ValidationError(f'Загруженное изображения меньше {models.Product.MIN_RESOLUTION[0]} px x {models.Product.MIN_RESOLUTION[1]} px') 
		if img.width > max_width or img.height > max_height:
			raise ValidationError(f'Загруженное изображения больше {models.Product.MAX_RESOLUTION[0]} px x {models.Product.MAX_RESOLUTION[1]} px')
		return image	


class NotebookAdmin(admin.ModelAdmin):
	
	form = ImageValidationAdminForm

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'category':
			kwargs['queryset'] = models.Category.objects.filter(slug='notebooks')
		return super().formfield_for_foreignkey(db_field, request, **kwargs)	


class SmartphoneAdmin(admin.ModelAdmin):
	
	form = ImageValidationAdminForm

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'category':
			kwargs['queryset'] = models.Category.objects.filter(slug='smartphones')
		return super().formfield_for_foreignkey(db_field, request, **kwargs)	


admin.site.register(models.Category),
admin.site.register(models.Notebook, NotebookAdmin)
admin.site.register(models.Smartphone, SmartphoneAdmin)
admin.site.register(models.Customer),
admin.site.register(models.Cart),

