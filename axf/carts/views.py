from django.core.cache import cache
from django.db.models import Sum
from django.shortcuts import render

from rest_framework import viewsets,mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response

from carts.models import Cart
from carts.serializer import *
from goods.models import Goods
from user.models import AXFUser
from utils import errors
from utils.UserAuthentication import UserAuth
from utils.login_required import is_login


class CartView(viewsets.GenericViewSet,mixins.UpdateModelMixin,mixins.ListModelMixin):
	queryset = Cart.objects.all()
	serializer_class = CartSerializer
	#用户登录认证方法 也可以用装饰器，中间件来实现，
	authentication_classes =(UserAuth,)
	#建议使用这种方法，因为会频繁使用到user, authentication会将uesr返回到request中，获取比较方便
	
	
	# @is_login
	def list(self, request, *args, **kwargs):
		# token = request.query_params.get('token', '')
		# user_id = cache.get(token)
		# user = AXFUser.objects.filter(pk=user_id).first()
		user=request.user
		queryset =self.get_queryset()
		queryset=queryset.filter(c_user=user)
		total_price=0
		serializer = self.get_serializer(queryset, many=True)
		
		for cart in queryset.filter(c_is_select=1):
			total_price+=cart.c_goods.price*cart.c_goods_num
		res={
			'carts':serializer.data,
			'total_price':total_price,
		}
		# res={
		# 	'code':200,
		# 	'msg':'请求成功',
		# 	'data':data
		# }
		return Response(res)
	
	
	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		# serializer = self.get_serializer(instance, data=request.data)
		# serializer.is_valid(raise_exception=True)
		instance.c_is_select= not instance.c_is_select
		instance.save()
		res={}
		return  Response(res)
	
	
	@list_route(methods=['POST'],serializer_class=AddCartSerializer)
	@is_login
	def add_cart(self,request):
		token=request.data.get('token','')
		# if not token:
		# 	raise errors.ParamsException({'code':1007,'msg':'请先登录'})
		goods_id=request.data.get('goodsid')
		user_id=cache.get(token)
		dict1={'c_user':user_id,'c_goods':goods_id}
		serializer=self.get_serializer(data=dict1)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		res={
			'code':200,
			'msg':'添加成功',
			'data':''
		}
		return Response(res)
	
	@list_route(methods=['POST'], serializer_class=SubCartSerializer)
	@is_login
	def sub_cart(self, request):
		token = request.data.get('token', '')
		# if not token:
		# 	raise errors.ParamsException({'code':1007,'msg':'请先登录'})
		goods_id = request.data.get('goodsid')
		user_id = cache.get(token)
		dict1 = {'c_user': user_id, 'c_goods': goods_id}
		serializer = self.get_serializer(data=dict1)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		res = {
			'code': 200,
			'msg': '减少成功',
			'data': ''
		}
		return Response(res)
	
	@list_route(methods=['PATCH'])
	# @is_login
	def change_all(self,request,*args,**kwargs):
		# token = request.data.get('token', '')
		# user_id = cache.get(token)
		# user = AXFUser.objects.filter(pk=user_id).first()
		user=request.user
		Cart.objects.filter(c_user=user).update(c_is_select=1)
		res={}
		return Response(res)
	
	
	
	
	
	# @list_route(methods=['POST'], serializer_class=AddCartSerializer)
	# def add_cart(self, request):
	# 	goods_id = request.data.get('goodsid')
	# 	user=request.user
	# 	user_id=user.id
	# 	dict1 = {'c_user': user_id, 'c_goods': goods_id}
	# 	serializer = self.get_serializer(data=dict1)
	# 	serializer.is_valid(raise_exception=True)
	# 	serializer.save()
	# 	res = {
	# 		'code': 200,
	# 		'msg': '添加成功',
	# 		'data': ''
	# 	}
	# 	return Response(res)

	
	
	
