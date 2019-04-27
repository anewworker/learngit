from flask import Blueprint, render_template, request

from back.models import Article, User, Category, Link
import math

web=Blueprint('web',__name__)

@web.route('/index/',methods=["GET"])
def index():
	#获取服务器里所有的文章列表
	all_article=len(Article.query.filter().all())
	count_page=math.ceil(len(Article.query.filter().all())/5)+1
	article_list=Article.query.filter().order_by(-Article.id).limit(5).all()
	user=User.query.filter(User.username=="袁满潭").first()
	category_list=Category.query.filter().order_by(Category.id).all()
	link_list=Link.query.filter().order_by(Link.id).all()

	#将数据传入模板并渲染
	return  render_template('web/index.html',title="最新发布",article_list=article_list,user=user,category_list=category_list,link_list=link_list,count_page=count_page,all_article=all_article)

@web.route('/index/<int:page>',methods=["GET"])
def get_article(page):
		all_article = len(Article.query.filter().all())
		count_page = math.ceil(len(Article.query.filter().all()) / 5) + 1
		article_list = Article.query.filter().order_by(-Article.id).offset((page - 1) * 5).limit(5).all()
		user = User.query.filter(User.username == "袁满潭").first()
		category_list = Category.query.filter().order_by(Category.id).all()
		link_list = Link.query.filter().order_by(Link.id).all()

		# 将数据传入模板并渲染
		return render_template('web/index.html', title="最新发布", article_list=article_list, user=user,
	category_list=category_list, link_list=link_list, count_page=count_page,all_article=all_article,page_now=page)






# @web.route('/article/',methods=["GET"])
# def article():
# 	title=request.args.get("title")
# 	article=Article.query.filter(Article.title==title).first()
# 	return render_template('web/article.html',title="详细资讯",article=article)
#这是两种不同的路由方式
@web.route('/article/<string:title>',methods=["GET"])
def article(title):
	title1=title
	article=Article.query.filter(Article.title==title).first()
	category_list = Category.query.filter().order_by(Category.id).all()
	link_list = Link.query.filter().order_by(Link.id).all()
	return render_template('web/article.html',title="详细资讯",article=article,title1=title1,category_list=category_list,link_list=link_list)

@web.route('/about/')
def about():
	link_list = Link.query.filter().order_by(Link.id).all()
	category_list = Category.query.filter().order_by(Category.id).all()
	return render_template('web/about.html',category_list=category_list,link_list=link_list)


# @web.route('/category/<string:category>')
# def category(category):
# 	categ=Category.query.filter(Category.c_name==category).first()
# 	article_list=categ.arts
# 	article_list.reverse()
# 	user = User.query.filter(User.username == "袁满潭").first()
# 	category_list = Category.query.filter().order_by(Category.id).all()
# 	title=category
# 	link_list = Link.query.filter().order_by(Link.id).all()
# 	return render_template('web/category.html',article_list=article_list,user=user,category_list=category_list,title=title,link_list=link_list)



@web.route('/<string:category>/<int:page>')
def category(category,page):
	categ=Category.query.filter(Category.c_name==category).first()
	#获取该分类的所有文章
	all_article=len(categ.arts)
	id=categ.id
	# print(id)
	article_list=Article.query.filter(Article.category_id==id).offset((page - 1) * 5).limit(5).all()
	# article_list.reverse()
	user = User.query.filter(User.username == "袁满潭").first()
	category_list = Category.query.filter().order_by(Category.id).all()
	title=category
	link_list = Link.query.filter().order_by(Link.id).all()
	count_page = math.ceil(all_article/ 5) + 1
	# article_list = Article.query.filter().order_by(-Article.id).offset((page - 1) * 5).limit(5).all()
	return render_template('web/category.html',article_list=article_list,user=user,category_list=category_list,title=title,link_list=link_list,count_page=count_page,page_now=page,all_article=all_article)


