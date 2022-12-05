from flask import Flask,request,jsonify
from flask_sqlalchemy import  SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__)


app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

app.config['SECRET_KEY']='619619'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # max size file

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)