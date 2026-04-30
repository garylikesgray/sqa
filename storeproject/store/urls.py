from django.urls import path
from . import views

# This tells Django which URL goes to which view
# 'store' is the app name (for naming URLs)

app_name = 'store'

urlpatterns = [
    # Homepage: /
    path('', views.home, name='home'),
    
    # Products page: /products/
    path('products/', views.products, name='products'),
    
    # Add to cart: /add-to-cart/<product_id>/
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    
    # Cart page: /cart/
    path('cart/', views.cart, name='cart'),
    
    # Remove from cart: /remove-from-cart/<item_index>/
    path('remove-from-cart/<int:item_index>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Checkout page: /checkout/
    path('checkout/', views.checkout, name='checkout'),
    
    # Order success: /order-success/
    path('order-success/', views.order_success, name='order_success'),
]

from django.urls import path
from .views import product_list

urlpatterns = [
    path('', product_list, name='product_list'),
]

