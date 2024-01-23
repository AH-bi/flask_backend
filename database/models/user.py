from database.database import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    pwd = db.Column(db.String(60), nullable=False)  # Adjusted length for hashed password
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.pwd = hashed_password

    def check_password(self, password):
        return bcrypt.check_password_hash(self.pwd, password)