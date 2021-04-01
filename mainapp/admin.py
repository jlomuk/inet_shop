from PIL import Image
from django.contrib import admin 
from django.forms import ModelForm, ValidationError
from django.utils.safestring import mark_safe

from . import models


class CustomAdminForm(ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['image'].help_text = mark_safe('<span style="color:red; font-size:12px;">\
			Загружайте изображение разрешением не менее чем {}x{} px и размером не более 2 мб,\
			 изображение свыше {}x{} px будет обрезано </span>'.format(\
				*models.Product.MIN_RESOLUTION, *models.Product.MAX_RESOLUTION
			)
		)
		instance = kwargs.get('instance')
		if not instance.sd:
			print(self.fields['sd_volume_max'])
			self.fields['sd_volume_max'].widget.attrs.update({
					'readonly': True, 'style': 'background:lightgrey;'
				})


	def clean_image(self):
		image = self.cleaned_data.get('image')
		img = Image.open(image)
		min_width, min_height = models.Product.MIN_RESOLUTION
		if image.size > models.Product.MAX_SIZE_IMAGE:
			raise ValidationError('Загруженное изображение превышает максимальное значение в 2 мб')
		if img.width < min_width or img.height < min_height:
			raise ValidationError(f'Загруженное изображения меньше {models.Product.MIN_RESOLUTION[0]} px x {models.Product.MIN_RESOLUTION[1]} px') 
		return image	





class NotebookAdmin(admin.ModelAdmin):
	
	form = CustomAdminForm

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'category':
			kwargs['queryset'] = models.Category.objects.filter(slug='notebooks')
		return super().formfield_for_foreignkey(db_field, request, **kwargs)	


class SmartphoneAdmin(admin.ModelAdmin):
	
	change_form_template = 'mainapp/admin.html'
	form = CustomAdminForm

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'category':
			kwargs['queryset'] = models.Category.objects.filter(slug='smartphones')
		return super().formfield_for_foreignkey(db_field, request, **kwargs)	


admin.site.register(models.Category),
admin.site.register(models.Notebook, NotebookAdmin)
admin.site.register(models.Smartphone, SmartphoneAdmin)
admin.site.register(models.Customer),
admin.site.register(models.Cart),
admin.site.register(models.CartProduct),

