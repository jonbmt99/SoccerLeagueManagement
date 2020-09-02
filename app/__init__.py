from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  flask_admin import Admin
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "\xa7#QV\x00\xb5rOf\x90P\xde@y\xb0\xa7"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Password123@localhost/soccerleaguemanagement?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)

admin = Admin(app=app, name="Quan ly giai dau bong da", template_mode="bootstrap3")

login = LoginManager(app=app)