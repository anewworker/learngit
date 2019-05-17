import re
import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from rest_framework import serializers

from user.models import AXFUser
from utils.errors import ParamsException


class Userserializer(serializers.ModelSerializer):


	class Meta:
		model=AXFUser
		fields='__all__'


class UserRegisterSerializer(serializers.Serializer):
	#注册序列化，起校验字段的作用，无需返回其他序列化数据
	u_username=serializers.CharField(required=True,max_length=10,min_length=4,error_messages={
		'required':'注册账号必填',
		'blank':'注册账号不能为空',
		'max_length':'最大长度为10字符',
		'min_length':'最小长度为4字符'
	})
	u_password=serializers.CharField(required=True,max_length=20,min_length=6,error_messages={
		'required':'注册密码必填',
		'blank': '注册密码不能为空',
		'max_length':'最大长度为10字符',
		'min_length':'最小长度为6字符'})
	u_password2=serializers.CharField(required=True,max_length=20,min_length=6,error_messages={
		'required':'确认密码必填',
		'blank': '确认密码不能为空',
		'max_length':'最大长度为10字符',
		'min_length':'最小长度为6字符'})
	u_email=serializers.EmailField(required=True,error_messages={
		'required':'注册邮箱必填',
		'blank': '注册邮箱不能为空',
		'invalid':'邮箱格式不正确',
	})

	def validate(self, attrs):
		username=attrs.get('u_username')
		pwd1=attrs.get('u_password')
		pwd2=attrs.get('u_password2')
		email=str(attrs.get('u_email'))
		if AXFUser.objects.filter(u_username=username).exists():
			raise ParamsException({'code':1001,'msg':"注册用户已存在"})
		if pwd1 != pwd2:
			raise ParamsException({'code':1002,'msg':"两次输入密码不一致"})

		# patterns ='^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$'
		# if not re.match(patterns,email):
		# 	# print(re.match(patterns,email))
		# 	raise ParamsException({'code':1003,'msg':'邮箱格式不正确，请确认'})
		return attrs

	def create(self, validated_data):
		username=validated_data.get('u_username')
		password=make_password(validated_data.get('u_password'))
		email=validated_data.get('u_email')
		user = AXFUser.objects.create(u_username=username,u_password=password,u_email=email)
		return user

	# def user_register(self,validated_data):
	# 	username = validated_data.get('u_username')
	# 	password=make_password(validated_data.get('u_password'))
	# 	email=validated_data.get('u_email')
	# 	user = AXFUser.objects.create(u_username=username,u_password=password,u_email=email)
	# 	return user


class UserLoginSerializer(serializers.Serializer):
	u_username = serializers.CharField(required=True, max_length=10, min_length=4, error_messages={
		'required': '登录账号必填',
		'blank': '登录账号不能为空',
		'max_length': '最大长度为10字符',
		'min_length': '最小长度为4字符'
	})
	u_password = serializers.CharField(required=True, max_length=20, min_length=6, error_messages={
		'required': '登录密码必填',
		'blank': '登录密码不能为空',
		'max_length': '最大长度为10字符',
		'min_length': '最小长度为6字符'})

	def validate(self, attrs):
		username=attrs.get('u_username')
		password=attrs.get('u_password')
		user=AXFUser.objects.filter(u_username=username).first()
		if not user:
			raise ParamsException({'code':1004,'msg':'用户不存在，请先注册'})
		if not check_password(password,user.u_password):
			raise ParamsException({'code':1005,'msg':'密码不正确，请确认密码'})
		return attrs

	def login_user(self,validated_data):
		#登录后，返回token给前端，并且保存到redis中
		token=uuid.uuid4().hex
		user=AXFUser.objects.filter(u_username=validated_data.get('u_username')).first()

		cache.set(token,user.id,timeout=24*60*60)
		return token

