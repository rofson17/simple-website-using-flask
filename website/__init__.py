from flask import Flask,  render_template

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os

load_dotenv()

DB = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    # app config
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.secret_key = os.getenv('SECRET_KEY')

    # database config
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    DB.init_app(app)

    from .models import Users, Contacts
    create_database(app)

    # handle urls
    from .urls import views
    app.register_blueprint(views)

    # handle 404 error
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    return app


def create_database(app):
    if not os.path.exists('website/'+DB_NAME):
        DB.create_all(app=app)
        print("Databse created!")
