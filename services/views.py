from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
    # Get the wanted category from database based on given id
    services = Service.objects.filter(category__id= request.data['id'])
    # Serialize the data to pass it as a response
    serializer = ServiceSerializer(services, many=True)
    # Return serialized data
    return Response(serializer.data)



# API EndPoint For view all services from database
@api_view(['POST'])
def ServiceList(request):
    # Get All Data from database
    services = ServiceVariant.objects.all()
    # serialize the data to pass it as a response
    serializer = ServiceVariantSerializer(services, many=True)
    # Return serialized data
    return Response(serializer.data)


# API EndPoint For View the details of one Service
@api_view(['POST'])
def ServiceDetails(request):
    # Get the wanted Service from database based on given id
    service = ServiceVariant.objects.filter(id= request.data['id']).first()
    # Serialize the data to pass it as a response
    serializer = ServiceVariantSerializer(service, many=False)
    # Return serialized data
    return Response(serializer.data)