from flask import Flask,render_template,url_for,session
from flask_script import Manager
import pymysql

from back.models import db
from web.views import web
from back.views import back

app=Flask(__name__)                          
app.secret_key='afsgdharewr'       

app.register_blueprint(blueprint=web,url_prefix='/web')
app.register_blueprint(blueprint=back,url_prefix='/back')

@app.route('/')
def index():
	return render_template('index.html')

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:337212@127.0.0.1:3306/mydb2'
db.init_app(app)

if __name__ == '__main__':
    manage=Manager(app)
    manage.run()