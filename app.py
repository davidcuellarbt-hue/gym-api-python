from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración para que el JSON se vea ordenado
app.config['JSON_SORT_KEYS'] = False

# --- CONFIGURACIÓN DE CONEXIÓN (Cámbialo por tus datos de TiDB) ---
USER = "4PdfpZzDzZDR2Ds.root"
PASS = "MHgBPuCbpoq8u853"
HOST = "gateway01.us-east-1.prod.aws.tidbcloud.com"
DB_NAME = "gym_db"

# 1. La URL de conexión base
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER}:{PASS}@{HOST}:4000/{DB_NAME}'

# 2. EL PARCHE DE SEGURIDAD (SSL): Esto soluciona el error OperationalError
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {
        "ssl": {
            "ca": "/etc/ssl/certs/ca-certificates.crt"
        }
    }
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELO ---
class Socio(db.Model):
    __tablename__ = 'Socio'
    idSocio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(100))

# --- RUTAS ---
@app.route('/')
def index():
    return jsonify({
        "status": "Online",
        "message": "API del Gimnasio funcionando con SSL",
        "endpoints": ["/socios"]
    })

@app.route('/socios', methods=['GET'])
def get_socios():
    try:
        socios = Socio.query.all()
        return jsonify([
            {"id": s.idSocio, "nombre": s.nombre, "email": s.correo} 
            for s in socios
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)