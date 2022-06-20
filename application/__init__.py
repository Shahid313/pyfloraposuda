from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import (LoginManager,UserMixin,login_user,login_required,
logout_user,current_user)

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret key"
# base directory path for sqlite databse
basedir = os.path.abspath(os.path.dirname(__file__))
# Integrating sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'databse.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'UserView:login'

# In models directory there is a models file from which all the models are imported
# application acts as main module for this project
from application.models.models import *
# In views directory there is a UserView file from which UserView class is imported 
# in which there are all the routes/apis related to user example: login, registeration, profile
from application.views.UserView import UserView
# In views directory there is a HomeView file from which HomeView class is imported 
# in which there are all the routes/apis related to home example: adding new plant, updating plant, 
# fetching all the plants e.t.c
from application.views.HomeView import HomeView

# The imported classes are registered here
UserView.register(app)
HomeView.register(app)