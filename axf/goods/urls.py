from django.urls import path
from rest_framework.routers import SimpleRouter

from goods.views import home,FoodTypeView,MarketView
# from goods.views import Home
router=SimpleRouter()
router.register('foodtype',FoodTypeView)
router.register('market',MarketView)
urlpatterns = [
	#函数形式，使用api_view装饰器
	path('home/',home),
	#继承APIView的形式
	# path('home2/',Home.as_view())
]

urlpatterns+=router.urls
