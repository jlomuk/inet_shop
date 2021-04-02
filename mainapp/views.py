from django.shortcuts import render
from django.views.generic import DetailView, View

from .models import Notebook, Smartphone, Category, LatestProducts, Customer, Cart
from .mixins import CategoryDetailMixin


class HomePageView(View):

	def get(self, request):
		categories = Category.objects.get_categories_for_left_sidebar()
		products = LatestProducts.objects.get_products_for_main_page('notebook', "smartphone", with_respect_to='notebook')
		context = {
			'categories' : categories,
			'products' : products,
		}
		return render(request, 'mainapp/base.html', context)


class ProductDetailView(CategoryDetailMixin, DetailView):

	CT_MODEL_CLASS = {
		'notebook': Notebook,
		'smartphone': Smartphone,
	}

	def dispatch(self, request, *args, **kwargs):
		self.model = self.CT_MODEL_CLASS.get(kwargs.get('ct_model'))
		return super().dispatch(request, *args, **kwargs)

	context_object_name = 'product'
	template_name = 'mainapp/product_detail.html'


class CategoryDetailView(CategoryDetailMixin, DetailView):

	models = Category
	queryset = Category.objects.all()
	context_object_name = 'category'
	template_name = 'mainapp/category_detail.html'
	slug_url_kwarg = 'slug'


class CartView(View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': cart,
            'categories': categories,
        }
        return render (request, "mainapp/cart.html", context)





























































































