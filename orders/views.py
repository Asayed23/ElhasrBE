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
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)
    serializer = CartItemSerializer(cart_items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def CartListOrCreate(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['POST'])
def AddToCart(request, pk):
    user = request.user
    cart = Cart.objects.get(user=user)
    service = ServiceVariant.objects.get(id=pk)
    quantity = 1
    cart_item = CartItem(cart=cart, item=service)
    cart_item.save()
    serializer = CartSerializer(cart)
    total = float(service.price) * float(quantity)
    cart.total_price += Decimal(total)
    cart.save()

    return Response(serializer.data)


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


@api_view(['DELETE'])
def CartItemDelete(request, pk):
    item = CartItem.objects.get(id=pk)
    item.delete()
    return Response('Item Deleted Succesfully')


@api_view(['POST'])
def CartView(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)