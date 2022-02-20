from django.db.models import fields
from rest_framework import serializers
from .models import Service, Category, ServiceVariant, ServiceAttribute


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = (
            'id',
            'name',
            'description',
            'category',
            'image',
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


class ServiceAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAttribute
        fields = (
            'service',
            'attr_name',
        )


class ServiceVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceVariant
        fields = (
            'service',
            'variant', 
            'price',
        )