from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin.contrib.sqla import ModelView

assignee = db.Table('assignee',
	db.Column('id', db.Integer, db.ForeignKey('user.id')),
	db.Column('ops_id', db.Integer, db.ForeignKey('ops.ops_id'))
)

class Ops(db.Model):
	ops_id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100000000)) 
	data = db.Column(db.String(100000000))
	date = db.Column(db.DateTime(timezone = True))
	url = db.Column(db.String(10000000000))
 

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	googleID = db.Column(db.String(150), unique=True)
	email = db.Column(db.String(150), unique=True)
	password = db.Column(db.String(150))
	first_name = db.Column(db.String(150))
	roles = db.Column(db.String(150))
	savedOps = db.relationship('Ops', secondary=assignee, backref=db.backref('savedOps', lazy='dynamic'))


