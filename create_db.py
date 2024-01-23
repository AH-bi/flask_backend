from database.database import create_app, db
from database.models.user import User

app = create_app()

# This script will create the database tables (for now one table will be created)
with app.app_context():
    db.create_all()
    print("Database tables created successfully.")

    # Sample users
    sample_users = [
        {"login": "user1", "password": "password1", "nom": "usern1", "prenom": "userp1"},
        {"login": "user2", "password": "password2", "nom": "usern2", "prenom": "userp2"},
        {"login": "user3", "password": "password3", "nom": "usern3", "prenom": "userp3"},
    ]

    for user_data in sample_users:
        new_user = User(login=user_data['login'], nom=user_data['nom'], prenom=user_data['prenom'])
        new_user.set_password(user_data['password'])
        db.session.add(new_user)

    db.session.commit()

    print("Sample users added successfully!!")
