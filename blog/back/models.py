from _datetime import datetime, date

from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class User(db.Model):

	username=db.Column(db.String(10),primary_key=True)
	password=db.Column(db.String(100))
	__tablename__='user'

class Category(db.Model):
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	c_name=db.Column(db.String(20),unique=True,nullable=False)
	arts=db.relationship("Article",backref="c")
	__table__name="category"

class Article(db.Model):
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	title=db.Column(db.String(20),unique=True,nullable=False)
	content=db.Column(db.Text)
	keywords=db.Column(db.String(20))
	describe=db.Column(db.String(100))
	date=db.Column(db.DateTime, default=datetime.now)
	img = db.Column(db.String(100),default='/static/image/sanmao.jpg')
	category_id=db.Column(db.Integer,db.ForeignKey("category.id"))

	__tablename__="article"

	# def __init__(self, title):
	# 	self.title = title
	# 	self.content=content
	# 	self.keywords=keywords
class Link(db.Model):
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	l_name=db.Column(db.String(50),nullable=True)
	l_url=db.Column(db.String(60),nullable=True)
	l_oname=db.Column(db.String(50),nullable=True)
	__tablename__='link'


