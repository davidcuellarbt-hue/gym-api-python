from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- CONFIGURACIÓN DE CONEXIÓN ---
# Reemplaza con tus credenciales de TiDB Cloud
USER = "4PdfpZzDzZDR2Ds.root"
PASS = "MHgBPuCbpoq8u853"
HOST = "gateway01.us-east-1.prod.aws.tidbcloud.com"
DB_NAME = "gym_db"

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER}:{PASS}@{HOST}:4000/{DB_NAME}'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {
        "ssl": {
            "ca": "/etc/ssl/certs/ca-certificates.crt"
        }
    }
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELOS (Ajustados a tu esquema final) ---

class Socio(db.Model):
    __tablename__ = 'Socio'
    idSocio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    fecha_inscripcion = db.Column(db.Date)  # Ahora está aquí según tu esquema
    correo = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    edad = db.Column(db.Integer)
    # Relación para que Flask entienda el vínculo con Membresía
    membresias = db.relationship('Membresia', backref='socio_rel', lazy=True)

class Membresia(db.Model):
    __tablename__ = 'Membresia'
    idMembresia = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    costo = db.Column(db.Float)
    tipo = db.Column(db.String(100))
    idSocio = db.Column(db.Integer, db.ForeignKey('Socio.idSocio'))

# --- RUTAS DE VISTA ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/socios')
def ver_socios():
    lista = Socio.query.all()
    return render_template('socios.html', socios=lista)

@app.route('/membresias')
def ver_membresias():
    # 1. Traemos las membresías unidas con los socios para mostrar NOMBRES en la tabla
    datos_tabla = db.session.query(Membresia, Socio).join(Socio).all()
    # 2. Traemos todos los socios para llenar el menú desplegable (Select) del formulario
    todos_los_socios = Socio.query.all()
    return render_template('membresias.html', datos=datos_tabla, socios=todos_los_socios)

# --- ACCIONES CRUD ---

@app.route('/agregar_socio', methods=['POST'])
def agregar_socio():
    nuevo = Socio(
        nombre=request.form.get('nombre'),
        fecha_inscripcion=request.form.get('fecha_inscripcion'),
        correo=request.form.get('correo'),
        telefono=request.form.get('telefono'),
        edad=request.form.get('edad')
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('ver_socios'))

@app.route('/agregar_membresia', methods=['POST'])
def agregar_membresia():
    nueva = Membresia(
        idSocio=request.form.get('idSocio'),
        tipo=request.form.get('tipo'),
        costo=request.form.get('costo'),
        fecha_inicio=request.form.get('fecha_inicio'),
        fecha_fin=request.form.get('fecha_fin')
    )
    db.session.add(nueva)
    db.session.commit()
    return redirect(url_for('ver_membresias'))

@app.route('/eliminar_socio/<int:id>')
def eliminar_socio(id):
    socio = Socio.query.get(id)
    if socio:
        # Primero eliminamos las membresías ligadas a ese socio para evitar errores de llave foránea
        Membresia.query.filter_by(idSocio=id).delete()
        db.session.delete(socio)
        db.session.commit()
    return redirect(url_for('ver_socios'))

@app.route('/eliminar_membresia/<int:id>')
def eliminar_membresia(id):
    mem = Membresia.query.get(id)
    if mem:
        db.session.delete(mem)
        db.session.commit()
    return redirect(url_for('ver_membresias'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
