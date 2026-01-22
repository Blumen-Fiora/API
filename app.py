from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

app = Flask(__name__)

# CORS erlauben, damit das Frontend (Port 443) mit dem Backend reden darf
CORS(app)

# JWT Konfiguration - Nutzt das Secret aus deiner .env oder einen Standardwert
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-geheim-uv-test")
jwt = JWTManager(app)

# Test-Datenbank (In-Memory)
users = {
    "admin": "geheim1234"
}

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Backend ist online", "secure": True}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username] == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "Falscher Benutzername oder Passwort"}), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Nur mit gültigem Token erreichbar
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user, message="Willkommen im sicheren Bereich!"), 200

@app.route('/data', methods=['GET'])
@jwt_required()
def get_data():
    # Diese Funktion wird aufgerufen, wenn GET /data kommt
    return jsonify({
        "message": "Erfolgreich angemeldet!",
        "user_data": "Hier sind deine geheimen Blumen-Fiora Infos"
    }), 200

# if __name__ == "__main__":
#     # Port 5000 muss mit deiner nginx.conf übereinstimmen
#     app.run(host="0.0.0.0", port=5000)
