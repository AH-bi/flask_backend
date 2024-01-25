from flask import session
from database.database import create_app, db
from routes.user_routes import main_routes
import secrets

app = create_app()

# Register the routes blueprint
app.register_blueprint(main_routes, url_prefix='/')

app.secret_key = secrets.token_hex(32)


if __name__ == '__main__':
    app.run(debug=True)