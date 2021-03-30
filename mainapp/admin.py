from django.contrib import admin
from . import models


admin.site.register(models.Category),
admin.site.register(models.Notebook)
admin.site.register(models.Smartphone)
admin.site.register(models.Customer),
admin.site.register(models.Product),
admin.site.register(models.Cart),
admin.site.register(models.CartProduct),
admin.site.register(models.Specification)