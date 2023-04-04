from flask import Flask
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tags import blp as TagBlueprint

from flask_jwt_extended import JWTManager
from db import db
import os


def create_app(db_url=None):
    app = Flask(__name__)

    # Flask-Smorest configuration
    # If there is an exception, Flask-Smorest will return a JSON response
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "1.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    # OPEN API SPECIFICATION
    # Flask-smorest uses Swagger UI to display the API documentation
    app.config["OPENAPI_URL_PREFIX"] = "/"
    # The path to the Swagger UI Documentation
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Database configuration
    # If the db_url is not None, then use it. Otherwise, use the DATABASE_URL environment variable
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the database
    db.init_app(app)
    api = Api(app)

    # JWT configuration
    app.config["JWT_SECRET_KEY"] = "jose"
    jwt = JWTManager(app)

    # Create the tables in the database. This is only needed if the tables do not exist
    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app
