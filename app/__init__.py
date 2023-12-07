from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = 'ImyYHNRCeaQQr7wnqAj4O_KMaqibso7gKegpojNmQsk'
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

from app import routes