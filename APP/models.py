from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(150), unique=True)    
    fullName = db.Column(db.String(150))
    password = db.Column(db.String(150))
    relevamiento = db.relationship('Relevamientos')

class Relevamientos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    base_id = db.Column(db.Integer, db.ForeignKey('base.id'))

class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base = db.Column(db.String(150))
    relevamientos = db.relationship('Relevamientos')

#prueba