from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from depto import Depto

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///gastos_comunes.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)

# CREA EL MODELO DE GASTOS COMUNES

class Gas_comunes(db.Model):
    idgc= db.Column(db.Integer, primary_key=True)
    iddepto= db.Column(db.Integer, db.ForeingKey('depto.iddepto'), nullable=False)
    ano= db.Column(db.Integer, nullable=False)
    mes= db.Column(db.Integer, nullable=False)
    fechap= db.Column(db.Date, nullable=False)
    valor= db.Column(db.Integer, nullable=False)
    pagado= db.Column(db.String(3), nullable=False)

    # RELACIONA CON LA TABLA DEPARTAMENTO
    depto= db.relationship('Depto', backref='Gas_comunes', lazy=True)

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

# SISTEMA CRUD GASTOS COMUNES

## CREA LOS GASTOS COMUNES

@app.route('/api/comunes', methods=['POST'])
@requiere_autenticacion
def crear_gasto():
    datos = request.get_json()
    nuevo_gasto = Gas_comunes(
        iddepto = int(datos['iddepto']),
        ano = int(datos['año']),
        mes = int(datos['mes']),
        fechap = int(datos['fecha_pago']),
        valor = int(datos['valor']),
        pagado = str(datos['pagado?'])
    )

    db.session.add(nuevo_gasto)
    db.session.commit()
    return jsonify({'mensaje': 'Gasto Comun agregado', 'id':nuevo_gasto.idgc})

## LECTURA DE LOS GASTOS COMUNES

@app.route('/api/comunes', methods=['GET'])
@requiere_autenticacion
def obtener_gastos():
    gasto = Gas_comunes.query.all()

    resultado= [
        {'id':g.idcg, 'iddepto':g.iddepto, 'ano':g.ano, 'mes':g.mes, 'fechap':g.fechap, 'valor':g.valor, 'pagado':g.pagado}
        for g in gasto
    ]
    return jsonify(resultado)

# LECTURA DE UN SOLO GASTO COMUN

@app.route('/api/comunes/<int:id>', methods=['GET'])
@requiere_autenticacion
def obtener_gasto(id):
    gasto = Gas_comunes.query.get(id)
    if not gasto:
        return jsonify({'mensaje': 'Gasto Comun no encontrado'}),404
    return jsonify({
        'id': gasto.idgc,
        'iddepto': gasto.iddepto,
        'ano': gasto.ano,
        'mes': gasto.mes,
        'fechap': gasto.fechap,
        'valor': gasto.valor,
        'pagado': gasto.pagado
    })

## ACTUALIZA LOS GASTOS COMUNES

@app.route('/api/comunes/<int:id>', methods=['PUT'])
@requiere_autenticacion
def actualizar_gasto(id):
    datos = request.get_json
    gasto = Gas_comunes.query.get(id)
    if not gasto:
        return jsonify({'mensaje': 'Gasto Comun no encontrado'}),404
    
    gasto.ano = datos.get('ano', gasto.ano)
    gasto.mes = datos.get('mes', gasto.mes)
    gasto.fechap = datos.get('fechap', gasto.fechap)
    gasto.valor = datos.get('valor', gasto.valor)
    gasto.pagado = datos.get('pagado', gasto.pagado)

    db.session.commit()
    return jsonify({'mensaje': 'Gasto Comun Modificado', 'id': gasto.idgc})

## ELIMINA EL GASTO COMUN

@app.route('/api/comunes/<int:id>', methods=['DELETE'])
@requiere_autenticacion
def eliminar_gasto(id):
    gasto = Gas_comunes.query.get(id)
    if not gasto:
        return jsonify({'mensaje': 'Gasto Comun no encontrado'}),404
    db.session.delete(gasto)
    db.session.commit()
    return jsonify({'mensaje': 'ERAI'}),401

## PERMITE EJECUTAR LA API

if __name__=='__main__':
    app.run(debug=True)
