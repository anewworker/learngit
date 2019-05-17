from django.core.cache import cache
from rest_framework import viewsets,mixins

from rest_framework.decorators import list_route
from rest_framework.response import Response

from user.models import AXFUser
from user.serializer import Userserializer, UserRegisterSerializer, UserLoginSerializer
from utils import errors



class UserView(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin):
	queryset = AXFUser.objects.all()
	serializer_class = Userserializer
	#返回登录用户信息
	def list(self, request, *args, **kwargs):
		# 1.获取前端传递的token值
		token=request.query_params.get("token")
		# 2.通过token从redis中找到对应用户id
		user_id = cache.get(token)
		user=AXFUser.objects.filter(id=user_id).first()
		# 3.序列化用户对象
		serializer=self.get_serializer(user)
		# print(user.od.all().filter(o_status=2).count())
		
		res={
			 'user_info':serializer.data,              #用户信息
			'orders_not_pay_num':user.od.all().filter(o_status=0).count(),      #用户下的订单信息
			'orders_not_send_num':user.od.all().filter(o_status=2).count(),
		}
		return  Response(res)



	@list_route(methods=['POST'],serializer_class=UserRegisterSerializer)
	def register(self,request):
		serializer=self.get_serializer(data=request.data)
		result=serializer.is_valid(raise_exception=False)
		if not result:
			raise errors.ParamsException({'code':1003,'msg':'参数校验失败','data':serializer.errors})
		user=serializer.save()
		# user=serializer.user_register(serializer.data)
		res={
			'code':200,
			'msg':"注册成功",
			'user_id':user.id
		}
		return Response(res)

	@list_route(methods=['POST'],serializer_class=UserLoginSerializer)
	def login(self,request):
		serializer=self.get_serializer(data=request.data)
		result=serializer.is_valid(raise_exception=False)
		if not result:
			raise errors.ParamsException({'code':1006,'msg':'参数校验失败' ,'data':serializer.errors})

		token=serializer.login_user(serializer.data)
		res = {
			'code':200,
			'msg':'登录成功',
			'token': token
		}

		return Response(res)

