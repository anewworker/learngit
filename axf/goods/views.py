import json

from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework import viewsets,mixins

from goods.models import Goods, MainWheel, MainNav, MainMustBuy, MainShow, MainShop, FoodType
from goods.serializer import *
from goods.filter import *

# class Home(APIView):
# 	def get(self,request):
# 		main_wheels = MainWheel.objects.all()
# 		main_navs = MainNav.objects.all()
# 		main_mustbuys = MainMustBuy.objects.all()
# 		main_shops = MainShop.objects.all()
# 		main_shows = MainShow.objects.all()
#
# 		res = {
# 			'main_wheels': MainWheelSerializer(main_wheels, many=True).data,
# 			'main_navs': MainNavSerializer(main_navs, many=True).data,
# 			'main_mustbuys': MainMustBuySerializer(main_mustbuys, many=True).data,
# 			'main_shops': MainShopSerializer(main_shops, many=True).data,
# 			'main_shows': MainShowSerializer(main_shows, many=True).data,
# 		}
#
# 		return Response(res)


@api_view(['GET'])
def home(request):
	#优化，使用redis进行缓存
	conn = get_redis_connection()
	if not conn.hget('goods','main_wheels'):
		mainwheels=MainWheel.objects.all()
		valueWheel=MainWheelSerializer(mainwheels,many=True).data
		valueWheel=json.dumps(valueWheel)
		conn.hset('goods','main_wheels',valueWheel)
	redis_main_wheels=json.loads(conn.hget('goods','main_wheels'))

	
	
	# main_wheels=MainWheel.objects.all()
	main_navs=MainNav.objects.all()
	main_mustbuys=MainMustBuy.objects.all()
	main_shops=MainShop.objects.all()
	main_shows=MainShow.objects.all()
	res={
		'main_wheels':redis_main_wheels,
		'main_navs':MainNavSerializer(main_navs,many=True).data,
		'main_mustbuys':MainMustBuySerializer(main_mustbuys,many=True).data,
		'main_shops':MainShopSerializer(main_shops,many=True).data,
		'main_shows':MainShowSerializer(main_shows,many=True).data,
	}
	
	return Response(res)
	

	
class FoodTypeView(viewsets.GenericViewSet,mixins.ListModelMixin):
	queryset= FoodType.objects.all()
	serializer_class = FoodTypeSerializer
	def list(self, request, *args, **kwargs):
		queryset=self.get_queryset()
		serializer = FoodTypeSerializer(queryset, many=True)
		res={
			'code':200,
			'msg':'请求成功',
			'data':serializer.data,
		}
		return Response(res)


class MarketView(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
	queryset = Goods.objects.all()
	serializer_class = GoodsSerializer
	filter_class=GoodsFilter
	def list(self, request, *args, **kwargs):
		queryset = self.filter_queryset(self.get_queryset())
		serializer = self.get_serializer(queryset, many=True)
		
		typeid=self.request.query_params.get('typeid')
		food_type=FoodType.objects.filter(typeid=typeid).first()
		#常规方式
		# child_list=[]
		# for childnames in food_type.childtypenames.split('#'):
		# 	data={
		# 		'chlid_name':childnames.split(':')[0] ,
		# 		'child_value':childnames.split(':')[1]
		# 	}
		# 	child_list.append(data)
		# foodtype_childname_list=child_list
		
		#列表推导式
		foodtype_childname_list=[{'child_name':childnames.split(':')[0],'child_value':childnames.split(':')[1]} for childnames in food_type.childtypenames.split('#')]
		
		order_rule_list=[
			{'order_name':'综合排序','order_value':0},
			{'order_name':'价格升序','order_value':1},
			{'order_name':'价格降序','order_value':2},
			{'order_name':'销量升序','order_value':3},
			{'order_name':'销量降序','order_value':4},
		]
		
		res = {
			'goods_list':serializer.data,
			'order_rule_list':order_rule_list,
			'foodtype_childname_list':foodtype_childname_list,
		}
		return Response(res)
	








