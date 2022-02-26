from dataclasses import fields
from rest_framework import serializers
from .models import Cart, CartItem
from services.models import ServiceVariant


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = (
            'id',
            'user',
            'total_price',
            'date_created'
        )


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'item',
            'cart'
        )
