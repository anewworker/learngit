import os
import random
from datetime import datetime
import time
from flask import Blueprint, render_template, request, session, redirect,url_for,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
import math

from back.models import db,User,Article,Category
from utls.function import login_required

back=Blueprint('back',__name__)


@back.route('/register/',methods=["GET",'POST'])
def register():
	if request.method=="GET":
		return render_template('back/register.html')
	#增加数据
	user=User()
	user.username=request.form.get('username')
	user.password=generate_password_hash(request.form.get("password"))
	#验证是否已经被注册
	if User.query.get(user.username) is None:
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('back.login'))
	return render_template('back/register.html')

@back.route("/check_register/",methods=["GET"])
def check_register():
	username=request.args.get("username")
	if User.query.filter(User.username==username).first():
		data={"0":"该用户已存在"}
		return jsonify(data)



@back.route('/login/',methods=["GET","POST"])
def login():
	if request.method=='GET':
		return render_template('back/login.html')
	if request.method=="POST":
		#获取从前端输入的数据
		username=request.form.get('username')
		password=request.form.get('password')
		print(username,password)
		#从数据库查找数据
		user=User.query.get(username)
		#判断账号密码是否匹配
		# print(check_password_hash(user.password,password))
		if username==user.username and check_password_hash(user.password,password):
			session['username']=username
			return redirect(url_for('back.index'))
	return render_template('back/login.html')

@back.route('/index/')
# @login_required
def index():
	username=session.get("username")
	if not username:
		return  render_template('back/login.html')
	count_art=len(Article.query.filter().all())
	count_user=len(User.query.filter().all())
	Datetime=datetime.now()
	return  render_template('back/index.html',title='index',count_art=count_art,count_user=count_user,datetime=Datetime,username=username)

# @back.route('/article/<int:page>',methods=["GET","POST"])
# @login_required
# def article(page):
# 	if request.method=="GET":
# 		# page=request.args.get("page")
# 		article_list=Article.query.filter().order_by(-Article.id).offset((page-1)*6).limit(6).all()
# 		count=len(article_list)
# 		all_page=math.ceil(len(Article.query.filter().all())/6)+1
# 		# print(all_page)
# 		return render_template('back/article.html', title="article",article_list=article_list,count=count,all_page=all_page)
	

@back.route('/article/',methods=["GET","POST"])
def Ajax_article():
	username=session.get("username")
	if request.method=="GET":
		if not request.args.get("page"):
			page=1
		# page = int(request.args.get("page", 1))
			article_list = Article.query.filter().order_by(-Article.id).offset((page - 1) * 6).limit(6).all()
			count = len(article_list)
			count_page = math.ceil(len(Article.query.filter().all()) / 6) + 1
			return render_template('back/article.html',article_list=article_list,count_page=count_page,title="article",username=username,count=count)
		else:
			page=int(request.args.get("page"))
			article_list = Article.query.filter().order_by(-Article.id).offset((page - 1) * 6).limit(6).all()
			# print(article_list)
			# print(page)
			art_dict={}
			for i in range(len(article_list)):
				data = {"title": article_list[i].title,
						  # "article.content":article_list[i].content,
						  "category":article_list[i].c.c_name,
						  "date":article_list[i].date
						  }
				art_dict[str(i+1)]=data

			count_page = math.ceil(len(Article.query.filter().all()) / 6) + 1
			# print(count_page)
			art_dict['count_page'] = count_page
			# print(art_dict)
			return jsonify(art_dict)
	if request.method=="POST":

		title=request.form.get("title")
		article=Article.query.filter(Article.title==title).first()
		img = article.img
		if img:
			new_img=os.path.split(img)[-1]
			path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'static/image/')
			# print(path)
			picture_path = os.path.join(path, new_img)
			os.remove(picture_path)
			db.session.delete(article)
			db.session.commit()
			data={"code":"删除成功"}
			return  jsonify(data)
		db.session.delete(article)
		db.session.commit()
		data = {"code": "删除成功"}
		return jsonify(data)







@back.route('/category/',methods=["GET","POST"])
@login_required
def category():
	if request.method=="GET":
		username=session.get('username')
		category_list=Category.query.filter().order_by(Category.id).all()
		return  render_template('back/category.html',title="category",category_list=category_list,username=username)
	if request.method=="POST":
		category_name=request.form.get("name")
		new_category=Category()
		new_category.c_name=category_name
		db.session.add(new_category)
		db.session.commit()
		return  redirect(url_for('back.category'))

@back.route('/update_category/<int:id>',methods=['GET',"POST"])
@login_required
def update_category(id):
	category=Category.query.filter(Category.id==id).first()
	id=category.id
	if request.method=="GET":
		# category = Category.query.filter(Category.c_name == c_name).first()
		c_id = category.id
		username = session.get('username')
		category_list = Category.query.filter().order_by(Category.id).all()
		return render_template('back/update_category.html',username=username,title="update_category",category=category,category_list=category_list)
	if request.method=="POST":
		category=Category.query.filter(Category.id==id).first()
		category.c_name=request.form.get("name")
		db.session.add(category)
		db.session.commit()
		return redirect(url_for('back.category'))



@back.route('/add_article/',methods=["GET","POST"])
@login_required
def add_article():
	# db.create_all()
	username=session.get("username")
	if request.method=="GET":
		category_list = Category.query.filter().order_by(Category.id).all()
		
		return render_template('back/add_article.html', title="add_article",category_list=category_list,username=username)
	if request.method=="POST":
		if request.files.get("picture"):
			picture = request.files.get("picture")
			new_filename=str(int(time.time()*1e10))[7::]+picture.filename
			picture_path = os.path.join('static/image/', new_filename)
			# print(picture_path)
			picture.save(picture_path)
			# print(type(picture_path))
			article=Article()
			article.title=request.form.get('title')
			article.describe=request.form.get('describe')
			article.content = request.form.get('content')
			article.keywords=request.form.get('keywords')
			article.category_id=request.form.get('category')

			article.img='/'+picture_path
			db.session.add(article)
			db.session.commit()
			return redirect(url_for('back.article'))
			# return redirect('/back/article/')
			# return render_template('back/article.html')
		else:
			article = Article()
			article.title = request.form.get('title')
			article.describe = request.form.get('describe')
			article.content = request.form.get('content')
			article.keywords = request.form.get('keywords')
			article.category_id = request.form.get('category')

			db.session.add(article)
			db.session.commit()
			return redirect(url_for('back.article'))


@back.route('/check_title/',methods=["GET"])
@login_required
def check_title():
	title=request.args.get("title")
	if Article.query.filter(Article.title==title).first():
		data={"0":"该标题已存在"}
		return jsonify(data)




@back.route('/update_article/<string:title>',methods=["GET","POST"])
@login_required

def update_article(title):
	global id
	if request.method=="GET":
		article = Article.query.filter(Article.title == title).first()
		id = article.id
		category_list = Category.query.filter().order_by(Category.id).all()
		# name=article.title
		# content=article.content
		# category_id=article.category_id
		return render_template('back/update_article.html',title="update_article",article=article,category_list=category_list)
	if request.method=="POST":
		article = Article.query.filter(Article.id == id).first()
		article.title = request.form.get("title")
		article.content = request.form.get("content")
		article.keywords = request.form.get("keywords")
		article.describe = request.form.get("describe")
		article.category_id = request.form.get("category")
		if request.files.get("picture"):
			picture=request.files.get("picture")
			new_filename = str(int(time.time() * 1e10))[7::] + picture.filename
			picture_path = os.path.join('static/image/', new_filename)
			print(picture_path)
			picture.save(picture_path)
			article.img = '/' + picture_path
		db.session.add(article)     
		db.session.commit()
		return redirect(url_for('back.article'))
		#
		# else:
		# 	article = Article.query.filter(Article.id == id).first()
		# 	article.title = request.form.get("title")
		# 	article.content = request.form.get("content")
		# 	article.keywords = request.form.get("keywords")
		# 	article.describe = request.form.get("describe")
		# 	article.category_id = request.form.get("category")
		# 	db.session.add(article)
		# 	db.session.commit()
		# 	return redirect(url_for('back.article'))



@back.route('/category/delete/',methods=["POST"])
@login_required
def delete_category():
	if request.method=="POST":
		id=int(request.form.get("id"))
		category=Category.query.filter(Category.id==id).first()
		#获取文章对象的列表，然后遍历删除
		for article in category.arts:
			db.session.delete(article)
		db.session.delete(category)
		db.session.commit()
		count=len(Category.query.filter().all())
		data={"count":count}
		return jsonify(data)
		# return redirect(url_for('back.category'))
		