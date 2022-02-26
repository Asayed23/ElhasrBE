from statistics import mode
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, help_text="Category Name", verbose_name="Category name")
    description = models.TextField(null=True, blank=True, help_text="Category Description", verbose_name="Category Description")
    image = models.ImageField(upload_to ='uploads/categories/', help_text="Image for Category",)
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# class Service(models.Model):
#     name = models.CharField(max_length=200, null=False, blank=False, help_text="Service Name", verbose_name="Service name")
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="The Category Name of the Service",)
#     description = models.TextField(null=True, blank=True, help_text="Service Description", verbose_name="Service Description")
#     price = models.FloatField(null=True, blank=True, verbose_name="Service Price")
#     image = models.ImageField(upload_to ='uploads/services/', help_text="Image For Service", verbose_name="Service image")

#     class Meta:
#         verbose_name = "Service"
#         verbose_name_plural = "Services"

#     def __str__(self):
#         return self.name

class Service(models.Model):
    """
    This model holds all common fields of a service
    """
    name = models.CharField(max_length=200, null=False, blank=False, help_text="Service Name", verbose_name="Service name")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="The Category Name of the Service",)
    description = models.TextField(null=True, blank=True, help_text="Service Description", verbose_name="Service Description")
    image = models.ImageField(upload_to ='uploads/services/', help_text="Image For Service", verbose_name="Service image")

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name


class ServiceAttribute(models.Model):
    """
    This model holds the attribute_name (ex: small)
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    attr_name = models.CharField(max_length=155, blank=True, help_text="size of the service", verbose_name="Size")

    class Meta:
        verbose_name = "Service Attribute"
        verbose_name_plural = "Service Attributes"

    def __str__(self):
        return self.service.name + " " + self.attr_name


class ServiceVariant(models.Model):
    """
    This model holds the values for price and combination of attributes
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    variant = models.ForeignKey(ServiceAttribute,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=25, decimal_places=2)

    class Meta:
        verbose_name = "Service Variant"
        verbose_name_plural = "Service Variants"

    def __str__(self):
        return self.service.name