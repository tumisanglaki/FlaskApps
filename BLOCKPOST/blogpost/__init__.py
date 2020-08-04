from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e1b2b80f3355e29c0bad27af726f5308cc2366e86915aabbcc0665f09f4b67fc'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:1laki2@localhost/Blogsite1'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cyberexpert2020@gmail.com'
app.config['MAIL_PASSWORD'] = 'ZXCVBNM<>'
mail = Mail(app)
from blogpost import routes
