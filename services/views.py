from multiprocessing import context
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Category, Service, ServiceVariant, ServiceAttribute
from .serializers import CategorySerializer, ServiceSerializer, ServiceAttributeSerializer, ServiceVariantSerializer


# API EndPoint For view all categories from database
@api_view(['POST'])
def CategoryList(request):
    # Get All Data from database
    categories = Category.objects.all()
    # serialize the data to pass it as a response
    serializer = CategorySerializer(categories, many=True)
    # Return serialized data
    return Response(serializer.data)


# API EndPoint For View the details of one category
@api_view(['POST'])
def CategoryDetails(request):
    # Get the user size
    size = int(request.data['size'])
    if size <= 500:
        size = 500
    elif 500 <size < 800:
        size = 800
    elif 800 < size:
        size = 1000
    

    # Get the wanted category from database based on given id
    services = Service.objects.filter(category__id= request.data['category_id'])

    # Serialize the data to pass it as a response
    serializer = ServiceSerializer(services, many=True)
    context = [
        {
        'service_id' : service['id'],
        'name': service['name'],
        'description':service['description'],
        'category': service['category'],
        'image': service['image'],
        'price': ServiceVariant.objects.get(service__id = service['id'], variant__attr_name = str(size)).price,
    }for service in serializer.data
    ]

    # Return serialized data
    return Response(context)



# # API EndPoint For View the details of one Service
# @api_view(['POST'])
# def ServiceDetails(request):
#     # Get the user size
#     size = int(request.data['size'])
#     if size <= 500:
#         size = 500
#     elif 500 <size < 800:
#         size = 800
#     elif 800 < size:
#         size = 1000
#     # Get the wanted Service from database based on given id
#     service = ServiceVariant.objects.filter(id= request.data['id'], variant__attr_name = str(size)).first()
#     service_details = Service.objects.get(name = service.service)
#     # Serialize the data to pass it as a response
#     serializer = ServiceVariantSerializer(service, many=False)
#     details_serializer = ServiceSerializer(service_details, many=False)
#     context = {
#         'variant': serializer.data,
#         'service': details_serializer.data,
#     }
#     # Return serialized data
#     return Response(context)
#     #return Response(serializer.data)