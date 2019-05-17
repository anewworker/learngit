from django.core.cache import cache
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins,viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from carts.models import Cart
from orders.models import Order, OrderGoods
from orders.serializre import *
from user.models import AXFUser
from utils import errors
from utils.UserAuthentication import UserAuth


# class OrderView(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):
# 	queryset = Order.objects.all()
# 	serializer_class = OrderSerializer
# 	authentication_classes = (UserAuth,)
	
	# {code:, msg:, data:{'order_goods':{obj1:{order_goods_info},obj2:{order_goods_info}} ,} }



@api_view(['GET','POST'])
def orders(request):
	if request.method=="POST":
		token=request.query_params.get('token')
		if not token:
			raise errors.ParamsException({'code':'1008','msg':'请先登录'})
		user_id=cache.get(token)
		user=AXFUser.objects.filter(pk=user_id).first()
		total_price=0
		cart_list=Cart.objects.filter(c_user=user,c_is_select=1).all()
		if not cart_list:
			raise errors.ParamsException({'code':1010,'msg':'购物车中没有商品'})
		# for cart in cart_list:
			# total_price += cart.c_goods.price * cart.c_goods_num
		total_price=sum([ cart.c_goods_num*cart.c_goods.price for cart in cart_list])
		orderobj=Order.objects.create(o_user=user,o_price=total_price)
		# for cart in cart_list:
			# OrderGoods.objects.create(o_order=orderobj,o_goods=cart.c_goods,o_goods_num=cart.c_goods_num)
		[OrderGoods.objects.create(o_order=orderobj,o_goods=cart.c_goods,o_goods_num=cart.c_goods_num) for cart in cart_list ]
		Cart.objects.filter(c_user=user).delete()
		res={
		    'code':200,
			'msg':'下单成功，正在配单...'
		}
		return Response(res)
		
	
	if request.method=="GET":
		token = request.query_params.get('token')
		if not token:
			raise errors.ParamsException({'code': '1009', 'msg': '请先登录'})
		user_id = cache.get(token)
		user = AXFUser.objects.filter(pk=user_id).first()
		o_status=request.query_params.get('o_status','')
		if o_status=='not_send':
			order_list = Order.objects.filter(o_user=user, o_status=2).order_by('-id').all()
		elif o_status=='not_pay':
			order_list=Order.objects.filter(o_user=user,o_status=0).order_by('-id').all()
		# elif o_status=='not_send':
		else:
			order_list = Order.objects.filter(o_user=user).order_by('-id').all()
		serializer=OrderSerializer(order_list,many=True)
		res={
			'data': serializer.data
		}
		return Response(res)

	
