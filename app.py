from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- CONFIGURACIÓN ---
USER = "4PdfpZzDzZDR2Ds.root"
PASS = "MHgBPuCbpoq8u853"
HOST = "gateway01.us-east-1.prod.aws.tidbcloud.com"
DB_NAME = "gym_db"

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER}:{PASS}@{HOST}:4000/{DB_NAME}'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"connect_args": {"ssl": {"ca": "/etc/ssl/certs/ca-certificates.crt"}}}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELOS ---
class Socio(db.Model):
    __tablename__ = 'Socio'
    idSocio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    edad = db.Column(db.Integer)

class Membresia(db.Model):
    __tablename__ = 'Membresia'
    idMembresia = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100))
    costo = db.Column(db.Float)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
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
    lista = Membresia.query.all()
    return render_template('membresias.html', membresias=lista)

# --- FUNCIONALIDAD CRUD ---

@app.route('/agregar_socio', methods=['POST'])
def agregar_socio():
    nuevo = Socio(
        nombre=request.form.get('nombre'),
        correo=request.form.get('correo'),
        telefono=request.form.get('telefono'),
        edad=request.form.get('edad')
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('ver_socios'))

@app.route('/eliminar_socio/<int:id>')
def eliminar_socio(id):
    socio = Socio.query.get(id)
    if socio:
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
