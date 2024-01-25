import unittest
from unittest.mock import patch, Mock,MagicMock
from flask import Flask
from routes.user_routes import main_routes  
import secrets

class UserRoutesTestCase(unittest.TestCase):

    @patch('routes.user_routes.User')  
    @patch('routes.user_routes.db.session')  
    def test_add_user(self, mock_session, mock_user):
        app = Flask(__name__)
        app.register_blueprint(main_routes)
        
        with app.test_client() as client:

            # Case 1: User added successfully
            mock_user.query.filter_by.return_value.first.return_value = None
            data_success = {'login': 'testuser', 'pwd': 'testpassword', 'nom': 'Test', 'prenom': 'User'}
            response_success = client.post('/adduser', json=data_success)
        
            self.assertEqual(response_success.status_code, 201)
                                

            # Case 2: Request with emtpy field 
            data_success = {'login': '', 'pwd': 'testpassword2', 'nom': 'Test', 'prenom': 'User'}
            response_success = client.post('/adduser', json=data_success)
            self.assertEqual(response_success.status_code, 400)



  
            # Case 2: User already exists
            data_exists = {'login': 'existinguser', 'pwd': 'testpassword3', 'nom': 'Existing', 'prenom': 'User'}
            mock_user.query.filter_by.return_value.first.return_value = Mock()  # Simulate existing user (even if we set True will still work)
            response_exists = client.post('/adduser', json=data_exists)
            self.assertEqual(response_exists.status_code, 409)

            # Additional assertions
            if response_exists.status_code == 409:
                self.assertIn('error', response_exists.json)
                self.assertEqual(response_exists.json['error'], 'Login already exists. Please choose a different login.')
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    @patch('routes.user_routes.User')  
    @patch('routes.user_routes.db.session')  
    def test_check_user(self, mock_session, mock_user):
        app = Flask(__name__)
        app.secret_key = secrets.token_hex(32)

        app.register_blueprint(main_routes)

        # Test checking a user without interacting with the actual database
        with app.test_client() as client:

            # Case 1: Missing required fields
            data_missing_fields = {}
            response_missing_fields = client.post('/checkuser', json=data_missing_fields)
            self.assertEqual(response_missing_fields.status_code, 400)

            # Case 2: Invalid login or password
            mock_user.query.filter_by.return_value.first.return_value = None
            data_invalid_user = {'login': 'test', 'pwd': 'incorrectpassword'}
            response_invalid_user = client.post('/checkuser', json=data_invalid_user)
            self.assertEqual(response_invalid_user.status_code, 401)

            # Case 3: Valid user and correct password
            mock_user_instance = MagicMock()
            mock_user_instance.nom = 'test'
            mock_user_instance.prenom = 'user'
            mock_user_instance.login= 'testuser'
            mock_user_instance.check_password.return_value = True
            mock_user.query.filter_by.return_value.first.return_value = mock_user_instance

            data_valid_user = {'login': 'testuser', 'pwd': 'correctpassword'}
            response_valid_user = client.post('/checkuser', json=data_valid_user)
            self.assertEqual(response_valid_user.status_code, 200)


            # Check the response content
            expected_response = {'login': 'testuser', 'nom': 'test', 'prenom': 'user'}
            self.assertDictEqual(response_valid_user.get_json(), expected_response)


  
if __name__ == '__main__':
    unittest.main()