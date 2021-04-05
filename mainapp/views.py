from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView, View
from django.contrib import messages

from .models import Notebook, Smartphone, Category, LatestProducts,\
                    Customer, Cart, CartProduct
from .mixins import CategoryDetailMixin, CartMixin


class HomePageView(CartMixin, View):

    def get(self, request):
        categories = Category.objects.get_categories_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_main_page('notebook', "smartphone", with_respect_to='notebook')
        context = {
            'categories' : categories,
            'products' : products,
            'cart': self.cart
        }
        return render(request, 'mainapp/base.html', context)


class ProductDetailView(DetailView):

    CT_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_CLASS.get(kwargs.get('ct_model'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     context['ct_model'] = self.model._meta.model_name
     return context 

    context_object_name = 'product'
    template_name = 'mainapp/product_detail.html'


class CategoryDetailView(CategoryDetailMixin, DetailView):

	models = Category
	queryset = Category.objects.all()
	context_object_name = 'category'
	template_name = 'mainapp/category_detail.html'
	slug_url_kwarg = 'slug'


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
                user=self.cart.owner, cart=self.cart, 
                content_type=content_type, object_id=product.id,
            )
        if created:
            self.cart.products.add(cart_product)
        self.cart.save()
        messages.add_message(request, messages.INFO, 'Товар добавлен в корзину')
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
                user=self.cart.owner, cart=self.cart, 
                content_type=content_type, object_id=product.id,
            )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        self.cart.save()
        messages.add_message(request, messages.INFO, 'Товар удален из корзины')
        return HttpResponseRedirect('/cart/')



class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': self.cart,
            'categories': categories,
        }
        return render (request, "mainapp/cart.html", context)


class ChangeQtyView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
                user=self.cart.owner, cart=self.cart, 
                content_type=content_type, object_id=product.id,
            )
        cart_product.qty = int(request.POST.get('qty'))
        cart_product.save()
        self.cart.save()
        messages.add_message(request, messages.INFO, 'Кол-во товара изменено')
        return HttpResponseRedirect('/cart/')


























































































