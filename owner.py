from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from depto import Depto

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///owner.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)

# CREA EL MODELO DE DEPARTAMENTO

class Owner(db.Model):
    idowner= db.Column(db.Integer, primary_key=True)
    o_nombre= db.Column(db.String(300), nullable=False)
    o_apelldo= db.Column(db.String(300), nullable=False)
    iddepto= db.Column(db.Integer, db.ForeignKey('Depto.iddepto'), nullable=False)

    # RELACIONA CON EL DEPARTAMENTO
    Depto= db.relationship('Depto', back_populates='owners')

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

# SISTEMA CRUD PROPIETARIO

## CREACION DE LOS PROPIETARIOS

@app.route('/api/owner', methods=['POST'])
@requiere_autenticacion
def crear_owner():
    datos = request.get_json()
    nuevo_owner = Owner(
        o_nombre = str(datos['nombre']),
        o_apelldo = str(datos['apellido']),
        iddepto = int(datos['iddepto'])
    )

    db.session.add(nuevo_owner)
    db.session.commit()
    return jsonify({'mensaje': 'Propietario creado', 'id':nuevo_owner.idowner})

## LECTURA DE LOS PROPIETARIOS

@app.route('/api/owner', methods=['GET'])
@requiere_autenticacion
def obtener_owners():
    owners= Owner.query.all()

    resultado= [
        {'id':o.itowner, 'nombre':o.o_nombre, 'apellido':o.o_apellido, 'iddepto':o.iddepto}
        for o in owners
    ]
    return jsonify(resultado)

# LECTURA DE UN SOLO PROPIETARIO

@app.route('/api/owner/<int:id>', methods=['GET'])
@requiere_autenticacion
def obtener_owner(id):
    owner = Owner.query.get(id)
    if not owner:
        return jsonify({'mensaje': 'Propietario no encontrado'}),404
    return jsonify({
        'id': owner.idowner,
        'nombre': owner.o_nombre,
        'apellido': owner.o_apellido,
        'iddepto' : owner.iddepto
    })

## ACTUALIZA LOS PROPIETARIOS

@app.route('/api/owner/<int:id>', methods=['PUT'])
@requiere_autenticacion
def actualizar_owner(id):
    datos = request.get_json()
    owner = Owner.query.get(id)
    if not owner:
        return jsonify({'mensaje': 'Propietario no encontrado'}),404
    
    owner.o_nombre = datos.get('nombre', owner.o_nombre)
    owner.o_apellido = datos.get('apellido', owner.o_apellido)
    owner.iddepto = datos.get('iddepto', owner.iddepto)

    db.session.commit()
    return jsonify({'mensaje': 'Propietario modificado', 'id': owner.idowner})

## ELIMINA EL PROPIETARIO

@app.route('/api/owner/<int:id>', methods=['DELETE'])
@requiere_autenticacion
def eliminar_owner(id):
    owner = Owner.query.get(id)
    if not owner:
        return jsonify({'mensaje': 'Propietario no encontrado'}),404
    db.session.delete(owner)
    db.session.commit()
    return jsonify({'mensaje': 'ERAI'}),401

## PERMITE EJECUTAR LA API

if __name__=='__main__':
    app.run(debug=True)