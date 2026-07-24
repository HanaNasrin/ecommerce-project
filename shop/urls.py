from django.urls import path
from . import views
from .views import ProductListView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('shop/', views.HomeView.as_view(), name='shop'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path("login/",auth_views.LoginView.as_view(template_name="shop/login.html"),name="login"),
    path("logout/",auth_views.LogoutView.as_view(next_page="login"),name="logout"),
    path("password-reset/",auth_views.PasswordResetView.as_view(template_name="shop/password_reset.html"),name="password_reset"),
    path("register/",views.register,name="register"),
    path("profile/",views.profile,name="profile"),
    path("payment/",views.payment,name="payment"
),
]
