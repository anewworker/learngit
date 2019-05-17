from functools import wraps

from utils import errors


def is_login(func):
	@wraps(func)
	#这里的a 指代cartview对象
	def check(a,request, *args, **kwargs):
		token = request.query_params.get('token') if request.query_params.get('token') else request.data.get('token')
		if not token:
			raise errors.ParamsException({'code': 1008,'msg': '请先登录'})
		
		return func(a,request,*args, **kwargs)
	
	return check
