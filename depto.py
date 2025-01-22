from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///depto.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)

# CREA EL MODELO DE DEPARTAMENTO

class Depto(db.Model):
    iddepto= db.Column(db.Integer, primary_key=True)
    pisos= db.Column(db.Integer)

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

# SISTEMA CRUD DEPARTAMENTO

## CREACION DE LOS DEPARTAMENTOS

@app.route('/api/depto', methods=['POST'])
@requiere_autenticacion
def crear_depto():
    datos = request.get_json()
    nuevo_dpto = Depto(
        pisos = int(datos['pisos'])
    )

    db.session.add(nuevo_dpto)
    db.session.commit()
    return jsonify({'mensaje': 'Departamento creado', 'id':nuevo_dpto.iddepto})

## LECTURA DE LOS DEPARTAMENTOS

@app.route('/api/depto', methods=['GET'])
@requiere_autenticacion
def obtener_deptos():
    deptos= Depto.query.all()
   
    resultado= [
        {'id':d.iddepto, 'pisos':d.pisos}
        for d in deptos
    ]
    return jsonify(resultado)

# LECTURA DE UN SOLO DEPARTAMENTO

@app.route('/api/depto/<int:id>', methods=['GET'])
@requiere_autenticacion
def obtener_depto(id):
    depto = Depto.query.get(id)
    if not depto:
        return jsonify({'mensaje': 'Departamento no encontrado'}),404
    return jsonify({
        'id': depto.iddepto,
        'pisos': depto.pisos
    })

## ACTUALIZA LOS DEPARTAMENTOS (NO CREO QUE SE USE PERO IGUAL TA)

@app.route('/api/depto/<int:id>', methods=['PUT'])
@requiere_autenticacion
def actualizar_depto(id):
    datos = request.get_json()
    depto = Depto.query.get(id)
    if not depto:
        return jsonify({'mensaje': 'Departamento no encontrado'}),404
    
    depto.pisos = datos.get('pisos', depto.pisos)

    db.session.commit()
    return jsonify({'mensaje': 'Departamento tuneao', 'id': depto.iddepto})

## ELIMINA EL DEPARTAMENTO

@app.route('/api/depto/<int:id>', methods=['DELETE'])
@requiere_autenticacion
def eliminar_depto(id):
    depto = Depto.query.get(id)
    if not depto:
        return jsonify({'mensaje': 'Departamento no encontrado'}),404
    db.session.delete(depto)
    db.session.commit()
    return jsonify({'mensaje': 'ERAI'}),404

## PERMITE EJECUTAR LA API

if __name__=='__main__':
    app.run(debug=True)