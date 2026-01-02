from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Para que el JSON se vea ordenado en el navegador
app.config['JSON_SORT_KEYS'] = False

# CONFIGURACIÓN DE CONEXIÓN (Cámbialo por tus datos de TiDB)
USER = "4PdfpZzDzZDR2Ds.root"
PASS = "MHgBPuCbpoq8u853"
HOST = "gateway01.us-east-1.prod.aws.tidbcloud.com"
DB_NAME = "gym_db"

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER}:{PASS}@{HOST}:4000/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la tabla Socio
class Socio(db.Model):
    __tablename__ = 'Socio'
    idSocio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(100))

@app.route('/')
def index():
    return jsonify({
        "status": "Online",
        "message": "API del Gimnasio funcionando correctamente",
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
    # Render asigna un puerto dinámico, esto es vital para que funcione
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)