from django.contrib import admin
from .models import Category, Service, ServiceAttribute, ServiceVariant

# Register your models here.
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(ServiceAttribute)
admin.site.register(ServiceVariant)