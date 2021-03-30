from django.contrib import admin
from . import models


class NotebookAdmin(admin.ModelAdmin):

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'category':
			kwargs['queryset'] = models.Category.objects.filter(slug='notebooks')
		return super().formfield_for_foreignkey(db_field, request, **kwargs)	


class SmartphoneAdmin(admin.ModelAdmin):

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
admin.site.register(models.Specification)

