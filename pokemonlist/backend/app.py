from flask import Flask, request, jsonify, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# Conexão MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["pokemon_db"]
teams_collection = db["user_teams"]
users_collection = db["users"]



# -------- Rotas da PokéAPI --------
@app.route('/pokemon/<name>', methods=['GET'])
def get_pokemon(name):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name.lower()}') # pegamos informações de um pokemon específico
    return jsonify(response.json())



# -------- Autenticação --------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_pw = generate_password_hash(data['password'])
    users_collection.insert_one({"username": data['username'], "password": hashed_pw})
    return jsonify({"message": "Usuário criado!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users_collection.find_one({"username": data['username']})
    if user and check_password_hash(user['password'], data['password']):
        session['user_id'] = str(user['_id'])
        return jsonify({"message": "Login bem-sucedido!"})
    return jsonify({"error": "Credenciais inválidas"}), 401



# -------- CRUD Times --------
@app.route('/team', methods=['POST'])
def create_team():
    if 'user_id' not in session:
        return jsonify({"error": "Não autenticado"}), 401
    teams_collection.insert_one({
        "user_id": session['user_id'],
        "pokemons": request.json['pokemons']  # Lista de IDs (ex: [25, 132, 6])
    })
    return jsonify({"message": "Time salvo!"}), 201




@app.route('/teams', methods=['GET'])
def get_teams():
    if 'user_id' not in session:
        return jsonify({"error": "Não autenticado"}), 401
    teams = list(teams_collection.find({"user_id": session['user_id']}))
    return jsonify({"teams": teams})

if __name__ == '__main__':
    app.run(debug=True)