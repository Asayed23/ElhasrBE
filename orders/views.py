from decimal import Decimal
from rest_framework import permissions
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from services.models import ServiceVariant
from .serializers import CartSerializer, CartItemSerializer
from .models import Cart, CartItem



@api_view(['POST'])
def ListCartItems(request):
    # user = request.user
    user = request.data['user_id']
    cart_items = CartItem.objects.filter(cart__user=user)
    cart = Cart.objects.get(user = user)
    cart_item_serializer = CartItemSerializer(cart_items, many=True)
    cart_serializer = CartSerializer(cart)
    context = {
        'cart items': cart_item_serializer.data,
        'cart': cart_serializer.data
    }
    return Response(context)


@api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
def CartView(request):
    # user = request.user
    user = request.data['user_id']
    cart = Cart.objects.get(user=user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['POST'])
def AddToCart(request):
    # user = request.user
    user = request.data['user_id']
    service_id = request.data['service_id']
    cart = Cart.objects.get(user=user)
    service = ServiceVariant.objects.get(id=service_id)
    quantity = 1
    if CartItem.objects.filter(cart=cart, item=service).exists():
      return Response({'message':"item already added"})  
    cart_item = CartItem(cart=cart, item=service)
    cart_item.save()
    serializer = CartSerializer(cart)
    total = float(service.price) * float(quantity)
    cart.total_price += total
    cart.save()
    cart_items = CartItem.objects.filter(cart__user=user)
    cart_item_serializer = CartItemSerializer(cart_items, many=True)
    cart_serializer = CartSerializer(cart)
    context = {
        'cart items': cart_item_serializer.data,
        'cart': cart_serializer.data
    }
    return Response(context)
    # return Response(serializer.data)


# @api_view(['POST'])
# def CartItemIncrease(request, pk):
#     item = CartItem.objects.get(id=pk)
#     item.quantity += 1
#     item.save()
#     serializer = CartItemSerializer(item)
#     return Response(serializer.data)


# @api_view(['POST'])
# def CartItemDecrease(request, pk):
#     item = CartItem.objects.get(id=pk)
#     if item.quantity == 1:
#         item.delete()
#     else:
#         item.quantity -= 1
#         item.save()
#     serializer = CartItemSerializer(item)
#     return Response(serializer.data)


@api_view(['POST'])
def CartItemDelete(request):
    service_id = request.data['service_id']
    user = request.data['user_id']
    item = CartItem.objects.get(item=service_id)
    cart = Cart.objects.get(user= user)
    item.delete()
    serializer = CartSerializer(cart)
    cart.total_price -= float(item.item.price)
    cart.save()
    cart_items = CartItem.objects.filter(cart__user=user)
    cart_item_serializer = CartItemSerializer(cart_items, many=True)
    cart_serializer = CartSerializer(cart)
    context = {
        'cart items': cart_item_serializer.data,
        'cart': cart_serializer.data
    }
    return Response(context)
    # return Response(serializer.data)


