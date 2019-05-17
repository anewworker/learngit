
from datetime import datetime

from django.utils.deprecation import MiddlewareMixin
import logging

logger=logging.getLogger()

class logMiddleware(MiddlewareMixin):
	def process_request(self,request):
		#初始请求时间
		request.init_time=datetime.now()



	def process_response(self,request,response):
		try:
		#耗时
			count_time=datetime.now()-request.init_time
			method=request.method
			path=request.path
			status_code=response.status_code
			content=len(response.content)
			logger.info('%sms %s %s %s %s' % (count_time, method, path, status_code, content))
		except Exception as e:
			logger.critical("系统错误：%s" % e)
		return response


