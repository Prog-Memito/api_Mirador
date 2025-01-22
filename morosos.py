from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from depto import Depto
from tenant import Tenant

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///moroso.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)

# CREA EL MODELO PARA LOS MOROSOS

class Morosos(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    iddepto= db.Column(db.Integer, db.ForeingKey('depto.iddepto'), nullable=False)
    piso = db.Column(db.Integer, nullable=False)
    t_nombre= db.Column(db.String(300), db.ForeingKey('tenant.t_nombre'), nullable=False)
    pagado= db.Column(db.String(2), nullable=False)
    moroso= db.Column(db.String(2), nullable=False)

    # RELACIONA CON EL DEPARTAMENTO
    depto= db.relationship('Depto', backref='', lazy=True)

    # RELACIONA CON EL RESIDENTE
    tenant= db.relationship('Tenant', backref='', lazy=True)

with app.app_context():
    db.create_all()