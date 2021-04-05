from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('products/<str:ct_model>/<str:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', views.AddToCart.as_view(), name='add_to_cart'),

]
