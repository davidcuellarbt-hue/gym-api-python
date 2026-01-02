from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configura tu conexión aquí:
# Formato: mysql+pymysql://USUARIO:PASSWORD@HOST:4000/gym_db
USER = "4PdfpZzDzZDR2Ds.root"
PASS = "MHgBPuCbpoq8u853"
HOST = "gateway01.us-east-1.prod.aws.tidbcloud.com"
DB_NAME = "gym_db"

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER}:{PASS}@{HOST}:4000/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición del Modelo (Tu tabla Socio)
class Socio(db.Model):
    __tablename__ = 'Socio'
    idSocio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(100))

@app.route('/')
def home():
    return jsonify({"mensaje": "API de Gimnasio en Python funcionando"})

@app.route('/socios', methods=['GET'])
def get_socios():
    try:
        lista_socios = Socio.query.all()
        return jsonify([{"id": s.idSocio, "nombre": s.nombre, "correo": s.correo} for s in lista_socios])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render usa la variable de entorno PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)