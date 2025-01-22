from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///staff.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)

# CREA EL MODELO DE DEPARTAMENTO

class Staff(db.Model):
    idstaff= db.Column(db.Integer, primary_key=True)
    s_nombre= db.Column(db.String(300), nullable=False)
    s_apellido= db.Column(db.String(300), nullable=False)
    funcion= db.Column(db.String(300), nullable=False)

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

# SISTEMA CRUD PERSONAL

## CREACION DE LOS PERSONAL

@app.route('/api/staff', methods=['POST'])
@requiere_autenticacion
def crear_staff():
    datos = request.get_json()
    nuevo_staff = Staff(
        s_nombre = str(datos['nombre']),
        s_apellido = str(datos['apellido']),
        funcion = int(datos['funcion'])
    )

    db.session.add(nuevo_staff)
    db.session.commit()
    return jsonify({'mensaje': 'Personal creado', 'id':nuevo_staff.idstaff})

## LECTURA DE LOS PERSONAL

@app.route('/api/staff', methods=['GET'])
@requiere_autenticacion
def obtener_staffs():
    staffs= Staff.query.all()

    resultado= [
        {'id':s.itstaff, 'nombre':s.s_nombre, 'apellido':s.s_apellido, 'funcion':s.funcion}
        for s in staffs
    ]
    return jsonify(resultado)

# LECTURA DE UN SOLO PERSONAL

@app.route('/api/staff/<int:id>', methods=['GET'])
@requiere_autenticacion
def obtener_staff(id):
    staff = Staff.query.get(id)
    if not staff:
        return jsonify({'mensaje': 'Personal no encontrado'}),404
    return jsonify({
        'id': staff.idstaff,
        'nombre': staff.s_nombre,
        'apellido': staff.s_apellido,
        'funcion' : staff.funcion
    })

## ACTUALIZA LOS PERSONAL

@app.route('/api/staff/<int:id>', methods=['PUT'])
@requiere_autenticacion
def actualizar_staff(id):
    datos = request.get_json()
    staff = Staff.query.get(id)
    if not staff:
        return jsonify({'mensaje': 'Personal no encontrado'}),404
    
    staff.s_nombre = datos.get('nombre', staff.s_nombre)
    staff.s_apellido = datos.get('apellido', staff.s_apellido)
    staff.funcion = datos.get('funcion', staff.funcion)

    db.session.commit()
    return jsonify({'mensaje': 'Personal modificado', 'id': staff.idstaff})

## ELIMINA EL PERSONAL

@app.route('/api/staff/<int:id>', methods=['DELETE'])
@requiere_autenticacion
def eliminar_staff(id):
    staff = Staff.query.get(id)
    if not staff:
        return jsonify({'mensaje': 'Personal no encontrado'}),404
    db.session.delete(staff)
    db.session.commit()
    return jsonify({'mensaje': 'ERAI'}),401

## PERMITE EJECUTAR LA API

if __name__=='__main__':
    app.run(debug=True)