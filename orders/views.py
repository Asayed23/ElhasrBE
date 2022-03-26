
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
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Q

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
        print(order.id)
        cart = get_object_or_404(Cart,user= user)

        cart.total_price=0
        cart.save()
        CartItem.objects.filter(cart=cart).update(cart='',order=order)

        return Response({"order number": order.id,"total price":order.final_price})

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


@api_view(['Get'])
# @login_required(redirect_field_name='/orders/web/Listorders/', login_url='/admin/')
def webListorders(request):
    order = Order.objects.all().values("id",
            "user_id__username",
            "coupon_used_id__coupon_code",
            "final_price",
            "status",
            "user_comment",
            "owner_comment",
            "requested_date",
            "modified_date")
    # if request.user.is_superuser:
    #     order = Order.objects.all().values()
    # else:
    #     order = "you are n't authorized"
    context = {
        
        'orders': order
    }
    return Response(context)


@api_view(['Get'])
# @login_required(redirect_field_name='/orders/web/Listorders/', login_url='/admin/')
def webSearchorders(request):
    query=request.data["searchWord"]
    order = Order.objects.filter(
        Q(id__icontains=query) |
            Q(user_id__username__icontains=query) |
            Q(coupon_used_id__coupon_code__icontains=query) |
            Q(final_price__icontains=query) |
            Q(status__icontains=query) |
            Q(user_comment__icontains=query) |
            Q(owner_comment__icontains=query) |
            Q(requested_date__icontains=query) |
            Q(modified_date__icontains=query) 
    ).values("id",
            "user_id__username",
            "coupon_used_id__coupon_code",
            "final_price",
            "status",
            "user_comment",
            "owner_comment",
            "requested_date",
            "modified_date")
    # if request.user.is_superuser:
    #     order = Order.objects.all().values()
    # else:
    #     order = "you are n't authorized"
    context = {
        
        'orders': order
    }
    return Response(context)


@api_view(['Get'])
# @login_required(redirect_field_name='/orders/web/Listorders/', login_url='/admin/')
def webOrderDetail(request):
    orderId=request.data["orderId"]
    order = Order.objects.filter(
        id=orderId
    ).values("id",
            "user_id__username",
            "coupon_used_id__coupon_code",
            "final_price",
            "status",
            "user_comment",
            "owner_comment",
            "requested_date",
            "modified_date")
    # if request.user.is_superuser:
    #     order = Order.objects.all().values()
    # else:
    #     order = "you are n't authorized"
    context = {
        
        'orders': order
    }
    return Response(context)