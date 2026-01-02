from flask import Flask, render_template, jsonify
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

# --- RUTAS ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/socios')
def ver_socios():
    lista_socios = Socio.query.all()
    return render_template('socios.html', socios=lista_socios)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
