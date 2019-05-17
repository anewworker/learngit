
from rest_framework.renderers import JSONRenderer

class MyJsonRenderer(JSONRenderer):
	def render(self, data, accepted_media_type=None, renderer_context=None):
		code=data.pop('code',200)
		msg=data.pop('msg',"请求成功")
		result=data.pop('data',data)
		#将浏览器所有响应状态码都改为200,以便返回自己定义的状态码
		response = renderer_context['response']
		response.status_code = 200
		res={
			'code':code,
			'msg':msg,
			'data':result
		}
		return super().render(res,accepted_media_type=None, renderer_context=None)

