import json

from rest_framework import serializers

from goods.serializer import GoodsSerializer
from orders.models import Order, OrderGoods


class OrSerializer(serializers.ModelSerializer):
	o_goods=GoodsSerializer()
	class Meta:
		model=OrderGoods
		fields='__all__'

# 1.用添加字段的方式重构结果

class OrderSerializer(serializers.ModelSerializer):
	order_goods_info=serializers.SerializerMethodField()
	class Meta:
		model=Order
		fields=['o_user','o_price','o_time','o_status','order_goods_info']
		#obj是对应的order对象
	def get_order_goods_info(self,orderobj):
		serializer=OrSerializer(orderobj.og.all(),many=True)
		return serializer.data

	

#2.用to_representation重构结果

# class  OrderSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model=Order
# 		fields = '__all__'
#       instance是对应的order对象
# 	def to_representation(self, instance):
# 		data = super().to_representation(instance)
# 		order_goods = instance.og.all()
# 		data['order_goods_info'] = OrSerializer(order_goods, many=True).data
# 		return data
