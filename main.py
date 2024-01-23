from flask import Flask
from database.database import create_app, db
from routes.user_routes import main_routes

app = create_app()

# Register the routes blueprint
app.register_blueprint(main_routes, url_prefix='/')


if __name__ == '__main__':
    app.run(debug=True)