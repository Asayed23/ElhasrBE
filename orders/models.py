from django.db import models
from decimal import Decimal
from django.db.models import F, Sum
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from services.models import ServiceVariant

# Create your models here.

class Cart(models.Model):
    """
    This model holds the shopping Cart items and total price for one user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


    def __str__(self):
        return str(self.user)



@receiver(post_save, sender=User)
def create_user_cart(sender, created, instance, *args, **kwargs):
    if created:
        Cart.objects.create(user=instance)



class CartItem(models.Model):
    """
    This model holds the shopping Cart items.
    """
    item = models.ForeignKey(ServiceVariant, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return self.item.__str__()