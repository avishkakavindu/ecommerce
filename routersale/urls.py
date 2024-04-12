"""
URL configuration for routersale project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),
    path('product/', views.PRODUCT, name='product'),
    path('products/<str:id>', views.PRODUCT_DETAIL_PAGE, name='product_detail'),
    path('', views.HOME, name='home'),
    path('search/', views.SEARCH, name='search'),
    path('contact/', views.CONTACT_PAGE, name='contact'),
    path('register/', views.HandleRegister, name='register'),
    path('login/', views.HandleLogin, name='login'),
    path('logout/', views.HandleLogout, name='logout'),
    
    # Cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart_detail/',views.cart_detail,name='cart_detail'),
    path('cart/cart_checkout/',views.Check_out,name='checkout'),
    path('cart/cart_checkout/placeorder/',views.PLACE_ORDER,name='placeorder'),

    path('paypal_gateway/checkout/', views.payment_checkout, name='checkout_payment'),
    path('paypal_gateway/create_payment/<int:order_id>', views.create_payment, name='create_payment'),
    path('paypal_gateway/execute_payment/<int:order_id>', views.execute_payment, name='execute_payment'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
