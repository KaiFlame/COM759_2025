import os
from flask import Flask, request, jsonify, session
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_cors import CORS
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

# Conexão MongoDB
uri = "mongodb+srv://admin:shantylilaxuri@cluster0.a4adle1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["pokemon_db"]


teams_collection = db["user_teams"]
users_collection = db["users"]

# Rotas da PokéAPI 
@app.route('/pokemon/<name>', methods=['GET'])
def get_pokemon(name):
    """Busca dados de um Pokémon na PokéAPI."""
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name.lower()}')
    return jsonify(response.json())

def serialize_user(user):
    user["_id"] = str(user["_id"])
    return user

@app.route("/api/users", methods=["GET"])
def get_users():
    users = users_collection.find()
    serialized_users = [serialize_user(user) for user in users]
    return jsonify(serialized_users)


@app.route('/register', methods=['POST'])
def register():
    """Cria um novo usuário no MongoDB."""
    data = request.get_json()
    
    # Verifica se o usuário já existe
    if users_collection.find_one({"username": data['username']}):
        return jsonify({"error": "Nome de usuário já existe"}), 400
        
    hashed_pw = generate_password_hash(data['password'])
    users_collection.insert_one({
        "username": data['username'],
        "email": data.get('email', ''),
        "password": hashed_pw
    })
    return jsonify({"message": "Usuário criado com sucesso!"}), 201



@app.route('/login', methods=['POST'])
def login():
    """Autentica o usuário e inicia sessão."""
    data = request.get_json()
    user = users_collection.find_one({"username": data['username']})
    
    if user and check_password_hash(user['password'], data['password']):
        session['user_id'] = str(user['_id'])  # Armazena o ID na session
        return jsonify({
            "message": "Login bem-sucedido!",
            "username": user['username']
        })
    return jsonify({"error": "Credenciais inválidas"}), 401



@app.route('/logout', methods=['POST'])
def logout():
    """Encerra a sessão do usuário."""
    session.pop('user_id', None)
    return jsonify({"message": "Logout bem-sucedido"})

@app.route('/check-auth', methods=['GET'])
def check_auth():
    if 'user_id' in session:
        user = db.users.find_one({'_id': session['user_id']})
        if user:
            return jsonify({
                'authenticated': True,
                'user': {
                    'username': user['username'],
                    'email': user['email']
                    # outros campos necessários
                }
            }), 200
    return jsonify({'authenticated': False}), 401



# Rotas de Times (CRUD Completo)
@app.route('/team', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_team():
    """Gerencia o time único do usuário"""
    if 'user_id' not in session:
        return jsonify({"error": "Não autenticado"}), 401
    
    user_id = session['user_id']
    
    if request.method == 'GET':
        # Retorna o time do usuário
        team = teams_collection.find_one({"user_id": user_id})
        if not team:
            return jsonify({"pokemons": []})
        return jsonify({"pokemons": team.get("pokemons", [])})
    
    elif request.method == 'POST' or request.method == 'PUT':
        # Adiciona ou atualiza o time do usuário
        data = request.get_json()
        pokemon = data.get('pokemon')
        
        if not pokemon:
            return jsonify({"error": "Pokémon não especificado"}), 400
            
        # Verifica se já existe um time
        team = teams_collection.find_one({"user_id": user_id})
        
        if team:
            # Verifica se o pokemon já está no time
            if pokemon['id'] in [p['id'] for p in team.get('pokemons', [])]:
                return jsonify({"error": "Pokémon já está no time"}), 400
                
            # Verifica se o time já tem 6 pokémons
            if len(team.get('pokemons', [])) >= 6:
                return jsonify({"error": "Time já está completo (6 pokémons)"}), 400
                
            # Atualiza o time
            teams_collection.update_one(
                {"user_id": user_id},
                {"$push": {"pokemons": pokemon}}
            )
        else:
            # Cria um novo time
            teams_collection.insert_one({
                "user_id": user_id,
                "pokemons": [pokemon]
            })
        return jsonify({"message": "Pokémon adicionado ao time!"}), 200
    
    elif request.method == 'DELETE':
        # Remove um pokémon do time
        pokemon_id = request.args.get('pokemon_id')
        if not pokemon_id:
            return jsonify({"error": "ID do Pokémon não especificado"}), 400
            
        teams_collection.update_one(
            {"user_id": user_id},
            {"$pull": {"pokemons": {"id": int(pokemon_id)}}}
        )
        return jsonify({"message": "Pokémon removido do time!"}), 200


@app.route('/teams', methods=['GET'])
def get_teams():
    """Lista todos os times do usuário logado."""
    if 'user_id' not in session:
        return jsonify({"error": "Não autenticado"}), 401
    teams = list(teams_collection.find({"user_id": session['user_id']}))
    return jsonify({"teams": teams})



@app.route('/team/<team_id>', methods=['DELETE'])
def delete_team(team_id):
    """Remove um time do MongoDB."""
    if 'user_id' not in session:
        return jsonify({"error": "Não autenticado"}), 401
    teams_collection.delete_one({"_id": team_id, "user_id": session['user_id']})
    return jsonify({"message": "Time deletado!"})




if __name__ == '__main__':
    app.run(debug=True)