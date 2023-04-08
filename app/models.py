"""Creates sql tables"""
from app import db
from datetime import datetime

class Cargo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    cargotype = db.Column(db.String(50), nullable=False)
    departure = db.Column(db.DateTime)
    arrival = db.Column(db.DateTime)
    ship_id = db.Column(db.Integer, db.ForeignKey('spaceship.id'), nullable=False)

class Spaceship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maxweight = db.Column(db.Float, nullable=False)
    captain_id = db.Column(db.Integer, db.ForeignKey('captain.id'), nullable=False)
    cargos = db.relationship('Cargo', backref='spaceship', lazy=True)

class Captain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    rank = db.Column(db.String(50), nullable=False)
    homeplanet = db.Column(db.String(50), nullable=False)
    spaceships = db.relationship('Spaceship', backref='captain', lazy=True)

