from django.urls import path
from .views import AddToCart, CartItemDelete, ListCartItems, CartView,CouponCheckApi, createOrderApi,\
    Listorders,orderdetail,webListorders,webSearchorders,webOrderDetail


urlpatterns = [
    path('cart/view/', CartView, name='Create'),
    path('cart/list/', ListCartItems, name='cart_list'),
    path('cart/add/', AddToCart, name='add_to_cart'),
    path('cart/delete/', CartItemDelete, name='delete'),
    path('cart/CouponCheck/', CouponCheckApi.as_view(), name='CouponCheck'),
    path('order/createOrder/', createOrderApi.as_view(), name='createOrder'),
    path('order/orderdetail/', orderdetail, name='orderdetail'),
    path('order/Listorders/', Listorders, name='Listorders'),
    path('web/Listorders/', webListorders, name='webListorders'),
    path('web/Searchorders/', webSearchorders, name='webSearchorders'),
    path('web/OrderDetail/', webOrderDetail, name='webOrderDetail'),


]