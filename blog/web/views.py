from flask import Blueprint, render_template, request

from back.models import Article, User, Category

web=Blueprint('web',__name__)

@web.route('/index/',methods=["GET"])
def index():
	#获取服务器里所有的文章列表
	article_list=Article.query.filter().order_by(-Article.id).limit(5).all()
	print(article_list)
	user=User.query.filter(User.username=="袁满潭").first()
	category_list=Category.query.filter().order_by(Category.id).all()
	#将数据传入模板并渲染
	return  render_template('web/index.html',title="最新发布",article_list=article_list,user=user,category_list=category_list)

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
	return render_template('web/article.html',title="详细资讯",article=article,title1=title1,category_list=category_list)

@web.route('/about/')
def about():
	category_list = Category.query.filter().order_by(Category.id).all()
	return render_template('web/about.html',category_list=category_list)


@web.route('/category/<string:category>')
def category(category):
	categ=Category.query.filter(Category.c_name==category).first()
	article_list=categ.arts
	article_list.reverse()
	user = User.query.filter(User.username == "袁满潭").first()
	category_list = Category.query.filter().order_by(Category.id).all()
	title=category
	return render_template('web/category.html',article_list=article_list,user=user,category_list=category_list,title=title)


