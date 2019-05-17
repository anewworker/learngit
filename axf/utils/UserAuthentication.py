from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication

from user.models import AXFUser
from utils import errors


class UserAuth(BaseAuthentication):
	# 用户登录认证方法，该方法必须返回元组（user,token）  返回的user,token会包含在request中
	def authenticate(self, request):
		# token= request.query_params.get('token')
		# if not token:
		# 	token=request.data.get("token")
		
		token = request.query_params.get('token') if request.query_params.get('token') else request.data.get('token')
		user_id = cache.get(token)
		if user_id:
			user = AXFUser.objects.filter(pk=user_id).first()
			return user, token
	
		raise errors.ParamsException({'code': 1007, 'msg': '请先登录'})
