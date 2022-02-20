from django.db import models
from django.contrib.auth.models import User
from services.models import ServiceVariant

# Create your models here.
class CartItem(models.Model):
    """
    This model holds the shopping Cart items.
    """
    item = models.OneToOneField(ServiceVariant, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return self.item.service.name

class Cart(models.Model):
    """
    This model holds the shopping Cart items and total price for one user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=25, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

   
    def calculate_total(self):
        pass


    def __str__(self):
        return self.user