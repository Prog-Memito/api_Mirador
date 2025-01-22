from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from depto import Depto

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///tenant.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)

# CREA EL MODELO DE DEPARTAMENTO

class Tenant(db.Model):
    idtenant= db.Column(db.Integer, primary_key=True)
    t_nombre= db.Column(db.String(300), nullable=False)
    t_apellido= db.Column(db.String(300), nullable=False)
    iddepto= db.Column(db.Integer, db.ForeignKey('Depto.iddepto'), nullable=False)

    # RELACIONA CON EL DEPARTAMENTO
    Depto= db.relationship('Depto', back_populates='tenants')

with app.app_context():
    db.create_all()

#  HACE SISTEMA DE AUTENTICACION

def requiere_autenticacion(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        auth = request.authorization
        if not auth or auth.username !='Admin' or auth.password !='Admin':
            return jsonify({"mensaje":"Autenticacion requerida"}),401
        return f(*args,**kwargs)
    return decorator

# HACE QUE EL USUARIO SE TENGA QUE AUTENTICAR PARA USAR EL SISTEMA

@app.route('/api/auth', methods=['GET'])
def autenticar():
    auth = request.authorization
    if not auth or auth.username !='Admin' or auth.password !='Admin':
        return jsonify({"mensaje":"Autenticacion exitosa muyayo"}),401
    return jsonify({'mensaje': 'Credenciales correctas'}),401

# SISTEMA CRUD ARRIENDATARIO

## CREACION DE LOS ARRIENDATARIOS

@app.route('/api/tenant', methods=['POST'])
@requiere_autenticacion
def crear_tenant():
    datos = request.get_json()
    nuevo_tenant = Tenant(
        t_nombre = str(datos['nombre']),
        t_apellido = str(datos['apellido']),
        iddepto = int(datos['iddepto'])
    )

    db.session.add(nuevo_tenant)
    db.session.commit()
    return jsonify({'mensaje': 'Arrendatario creado', 'id':nuevo_tenant.idtenant})

## LECTURA DE LOS ARRIENDATARIOS

@app.route('/api/tenant', methods=['GET'])
@requiere_autenticacion
def obtener_tenants():
    tenants= Tenant.query.all()

    resultado= [
        {'id':t.ittenant, 'nombre':t.t_nombre, 'apellido':t.t_apellido, 'iddepto':t.iddepto}
        for t in tenants
    ]
    return jsonify(resultado)

# LECTURA DE UN SOLO ARRIENDATARIO

@app.route('/api/tenant/<int:id>', methods=['GET'])
@requiere_autenticacion
def obtener_tenant(id):
    tenant = Tenant.query.get(id)
    if not tenant:
        return jsonify({'mensaje': 'Arriendatario no encontrado'}),404
    return jsonify({
        'id': tenant.idtenant,
        'nombre': tenant.t_nombre,
        'apellido': tenant.t_apellido,
        'iddepto' : tenant.iddepto
    })

## ACTUALIZA LOS ARRIENDATARIOS

@app.route('/api/tenant/<int:id>', methods=['PUT'])
@requiere_autenticacion
def actualizar_tenant(id):
    datos = request.get_json()
    tenant = Tenant.query.get(id)
    if not tenant:
        return jsonify({'mensaje': 'Arriendatario no encontrado'}),404
    
    tenant.t_nombre = datos.get('nombre', tenant.t_nombre)
    tenant.t_apellido = datos.get('apellido', tenant.t_apellido)
    tenant.iddepto = datos.get('iddepto', tenant.iddepto)

    db.session.commit()
    return jsonify({'mensaje': 'Arriendatario modificado', 'id': tenant.idtenant})

## ELIMINA EL ARRIENDATARIO

@app.route('/api/tenant/<int:id>', methods=['DELETE'])
@requiere_autenticacion
def eliminar_tenant(id):
    tenant = Tenant.query.get(id)
    if not tenant:
        return jsonify({'mensaje': 'Arriendatario no encontrado'}),404
    db.session.delete(tenant)
    db.session.commit()
    return jsonify({'mensaje': 'ERAI'}),401

## PERMITE EJECUTAR LA API

if __name__=='__main__':
    app.run(debug=True)