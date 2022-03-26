
from decimal import Decimal
from rest_framework import permissions
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from services.models import ServiceVariant
from .serializers import CartSerializer, CartItemSerializer
from .models import Cart, CartItem,Coupon, Order
from django.contrib.auth.models import User
from datetime import date,datetime


@api_view(['POST'])
def ListCartItems(request):
    # user = request.user
    user = request.data['user_id']
    cart_items = CartItem.objects.filter(cart__user=user).values('item',
                'item__service__name','item__service__category',
                'item__service__description','item__service__image','item__price')
    cart = Cart.objects.get(user = user)
    # cart_item_serializer = CartItemSerializer(cart_items, many=True)
    cart_serializer = CartSerializer(cart)
    context = {
        'cart items': cart_items,
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
    cart = Cart.objects.get(user= user)
    item = CartItem.objects.get(item=service_id,cart=cart)
    # cart = Cart.objects.get(user= user)
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

class CouponCheckApi(APIView):
    # permission_classes = ()  # <-- And here


    def post(self, request, *args, **kwargs):

        if Coupon.objects.filter(

                coupon_code=request.data['coupon_code']).exists():
            coupon_res=Coupon.objects.filter(

            coupon_code=request.data['coupon_code']).values()

            return Response({"Data":coupon_res[0],
                            "status":True,
                            })
        else:
            return Response({"status":False,"Data": "Coupon not exist"})



class createOrderApi(APIView):
    # permission_classes = ()  # <-- And here


    def post(self, request, *args, **kwargs):

        user = request.data['user_id']
        user=User.objects.get(id=user)

        user_comment=request.data['user_comment']
        if 'coupon_code' in request.data:
            coupon_code=request.data['coupon_code']
            if Coupon.objects.filter(coupon_code=coupon_code).exists():

                coupon_used=Coupon.objects.get(coupon_code=coupon_code)

                discount_percent=Coupon.objects.filter(coupon_code=coupon_code).values_list("discount_percent", flat=True)[0]
            else:
                discount_percent=0
                coupon_used=None
        total_price = Cart.objects.filter(user=user).values_list("total_price", flat=True)[0]
        discounted_price=total_price*(1-discount_percent/100)
        order = Order(coupon_used=coupon_used, user=user,status='Requested',
                        final_price=discounted_price,user_comment=user_comment,
                        requested_date=datetime.now()
                        )
        order.save()
        # print(order.id)
        cart = get_object_or_404(Cart,user= user)

        CartItem.objects.filter(cart=cart).update(cart='',order=order)

        return Response({"Data": "order updated successfully"})

@api_view(['POST'])
def orderdetail(request):
    # user = request.user
    order = request.data['order_id']
    # user = request.data['user_id']
    cart_items = CartItem.objects.filter(order=order).values('item',
                'item__service__name','item__service__category',
                'item__service__description','item__service__image','item__price')
    order = Order.objects.filter(id = order).values()
    context = {
        'cart items': cart_items,
        'cart': order
    }
    return Response(context)



@api_view(['POST'])
def Listorders(request):
    # user = request.user
    # order = request.data['order_id']
    user = request.data['user_id']
    # cart_items = CartItem.objects.filter(order=order).values('item',
    #             'item__service__name','item__service__category',
    #             'item__service__description','item__service__image','item__price')
    order = Order.objects.filter(user__id = user).values()
    context = {
        # 'cart items': cart_items,
        'orders': order
    }
    return Response(context)