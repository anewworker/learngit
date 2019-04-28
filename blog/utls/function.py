from flask import session,render_template,redirect,url_for
from functools import wraps
def login_required(func):
	@wraps(func)
	#  @wraps接受一个函数来进行装饰，并加入了复制函数名称、注释文档、参数列表等等的功能。这可以让我们在装饰器里面访问在装饰之前的函数的属性。
	def check(*args,**kargs):
		try:
			#已经登录的情况
			username=session['username']
			return  func(*args,**kargs)
		except:
			#未登录的情况
			return  redirect(url_for("back.login"))
			# return render_template('back/login.html')
	return check