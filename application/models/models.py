from application import db
from flask_login import (LoginManager,UserMixin,login_user,login_required,
logout_user,current_user)

class User(db.Model,UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(55), nullable=False)
	password = db.Column(db.String(200))
	plant = db.relationship('Plants',backref='user', lazy='dynamic')


class Plants(db.Model):
    plant_id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String(250), nullable=False)
    line_one = db.Column(db.Text, nullable=False)
    line_two = db.Column(db.Text, nullable=False)
    line_three = db.Column(db.Text, nullable=False)
    line_four = db.Column(db.Text, nullable=False)
    line_five = db.Column(db.Text, nullable=False)
    plant_image = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))