from django.db import models


def  recalc_cart(cart):
	cart_data = cart.products.aggregate(
		models.Sum('final_price'), 
		models.Sum('qty')
	)
	cart.final_price =  cart_data.get('final_price__sum')
	if not cart.final_price:
		cart.final_price = 0
	cart.total_products  = cart_data.get('qty__sum')
	if not cart.total_products:
		cart.total_products = 0
	cart.save()