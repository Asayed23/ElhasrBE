from django.urls import path
from .views import AddToCart, CartItemDelete, ListCartItems, CartView


urlpatterns = [
    path('cart/view/', CartView, name='Create'),
    path('cart/list/', ListCartItems, name='cart_list'),
    path('cart/add/', AddToCart, name='add_to_cart'),
    path('cart/delete/', CartItemDelete, name='delete'),
]