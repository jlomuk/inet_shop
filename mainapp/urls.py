from django.urls import path
from django.contrib.auth.views import LogoutView


from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('products/<str:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('delete-from-cart/<str:slug>/', views.DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:slug>/', views.ChangeQtyView.as_view(), name='change_qty'),
    path('cheakout/', views.CheckoutView.as_view(), name='checkout'),
    path('make-order/', views.MakeOrderView.as_view(), name='make_order'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'), 
    path('profile/', views.ProfileView.as_view(), name='profile'), 

]
