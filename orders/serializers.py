from dataclasses import fields
from rest_framework import serializers
from .models import Cart, CartItem
from services.models import ServiceVariant,Category


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = (
            'id',
            'user',
            'total_price',
            'date_created',
        )


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = (
            'id',
            'item',
            'cart'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name', 
            'image', 
            'description'
        )
