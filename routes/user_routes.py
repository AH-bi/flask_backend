from flask import Blueprint, request, jsonify
from database.database import db
from database.models.user import User
from flask import session
import json
from unittest.mock import MagicMock

main_routes = Blueprint('main_routes', __name__)



# Custome class to avoid (jsonify serializable problem)
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MagicMock):
            return repr(obj)
        return super().default(obj)

@main_routes.route('/adduser', methods=['POST'])
def add_user():
    try:
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

        # Setting up session   
        
        """
            session['user_id'] = user.id
            session['user_login'] = user.login
        """

        # Extract user details
        user_details = {'login': new_user.login, 'nom': new_user.nom, 'prenom': new_user.prenom}
        #return CustomJSONEncoder().encode({'message': 'User added successfully', 'user': user_details}), 201
        return CustomJSONEncoder().encode({'message': 'User added successfully', 'user': user_details}), 201

    except Exception as e:
        print(f"Error in add_user: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500


@main_routes.route('/checkuser', methods=['POST'])
def check_user():
    try:
        data = request.get_json()

        if 'login' not in data or 'pwd' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        user = User.query.filter_by(login=data['login']).first()

        if user and user.check_password(data['pwd']):
                    
            # Setting up session   
            """
            session['user_id'] = user.id
            session['user_login'] = user.login
            """

        
            
            return jsonify({'nom': user.nom, 'prenom': user.prenom, 'login': user.login}), 200
        else:
            return jsonify({'error': 'Invalid login or password'}), 401
    except Exception as e:
        print(f"Error in check_user: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500
