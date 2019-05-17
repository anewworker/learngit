
from rest_framework import serializers

from carts.models import Cart
from goods.serializer import GoodsSerializer
from utils import errors


class CartSerializer(serializers.ModelSerializer):
	c_goods=GoodsSerializer()
	class Meta:
		model=Cart
		fields='__all__'
		
		
		

class  AddCartSerializer(serializers.ModelSerializer):
	# c_goods_id = serializers.CharField(required=True)
	# c_user_id = serializers.CharField(required=True)
	class Meta:
		model=Cart
		fields='__all__'
	def create(self, validated_data):
		user=validated_data.get('c_user')
		goods=validated_data.get('c_goods')
		cart=Cart.objects.filter(c_user=user,c_goods=goods).first()
		if cart:
			cart.c_goods_num+=1
			cart.save()
		else:
			Cart.objects.create(**validated_data)
		return  user
		

class SubCartSerializer(serializers.ModelSerializer):
	class Meta:
		model=Cart
		fields='__all__'
	
	def create(self, validated_data):
		user = validated_data.get('c_user')
		goods = validated_data.get('c_goods')
		cart = Cart.objects.filter(c_user=user, c_goods=goods).first()
		if cart:
			if cart.c_goods_num>1:
				cart.c_goods_num -= 1
				cart.save()
			else:
				Cart.objects.filter(c_user=user,c_goods=goods).delete()
		else:
			raise errors.ParamsException({'code':1009,'msg':'购物车中没有这件商品'})
		return user
		
		
		
		

