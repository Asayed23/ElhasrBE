from django.contrib import admin
from .models import CartItem, Cart,Order,Coupon

# Register your models here.
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Coupon)
admin.site.register(Order)