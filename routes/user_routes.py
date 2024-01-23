from flask import Blueprint, request, jsonify
from database.database import db
from database.models.user import User

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/adduser', methods=['POST'])
def add_user():
    data = request.get_json()

    # Check if required fields are present
    if 'login' not in data or 'pwd' not in data or 'nom' not in data or 'prenom' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if any fields are empty
    if any(value == '' for value in data.values()):
        return jsonify({'error': 'Empty fields not allowed'}), 400

    # Check if the login already exists
    existing_user = User.query.filter_by(login=data['login']).first()
    if existing_user:
        return jsonify({'error': 'Login already exists. Please choose a different login.'}), 409

    # Hash the password 
    new_user = User(login=data['login'], nom=data['nom'], prenom=data['prenom'])
    new_user.set_password(data['pwd'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User added successfully'}), 201




@main_routes.route('/checkuser', methods=['POST'])
def check_user():
    data = request.get_json()

    if 'login' not in data or 'pwd' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    user = User.query.filter_by(login=data['login']).first()

    if user and user.check_password(data['pwd']):
        return jsonify({'nom': user.nom, 'prenom': user.prenom, 'login': user.login}), 200
    else:
        return jsonify({'error': 'Invalid login or password'}), 401