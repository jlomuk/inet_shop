from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView, View
from django.contrib import messages

from .models import Category, Product ,Customer, Cart, CartProduct
from .mixins import CartMixin
from .forms import OrderForm
from .utils import recalc_cart


class HomePageView(CartMixin, View):

    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {
            'categories' : categories,
            'products' : products,
            'cart': self.cart
        }
        return render(request, 'mainapp/base.html', context)


class ProductDetailView(CartMixin, DetailView):

    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     context['cart'] = self.cart
     return context 

    context_object_name = 'product'
    template_name = 'mainapp/product_detail.html'


class CategoryDetailView(CartMixin, DetailView):

    models = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'mainapp/category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context 


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Товар добавлен в корзину')
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Товар удален из корзины')
        return HttpResponseRedirect('/cart/')



class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories,
        }
        return render(request, "mainapp/cart.html", context)


class ChangeQtyView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
                user=self.cart.owner, cart=self.cart, product=product
        )
        cart_product.qty = int(request.POST.get('qty'))
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Кол-во товара изменено')
        return HttpResponseRedirect('/cart/')


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form,
        }
        return render (request, "mainapp/checkout.html", context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Наш менеджер свяжется с Вами')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')























































































