from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- CONFIGURACIÓN DE CONEXIÓN ---
USER = "4PdfpZzDzZDR2Ds.root"
PASS = "MHgBPuCbpoq8u853"
HOST = "gateway01.us-east-1.prod.aws.tidbcloud.com"
DB_NAME = "gym_db"

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER}:{PASS}@{HOST}:4000/{DB_NAME}'
# Parche SSL para Render/Linux
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {
        "ssl": {
            "ca": "/etc/ssl/certs/ca-certificates.crt"
        }
    }
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELOS (ORM) ---
class Socio(db.Model):
    __tablename__ = 'Socio'
    idSocio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(100))

class Membresia(db.Model):
    __tablename__ = 'Membresia'
    idMembresia = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100))
    costo = db.Column(db.Float)

# --- RUTAS ---
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

