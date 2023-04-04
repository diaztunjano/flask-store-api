from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    jwt_required,
)
from blocklist import BLOCKLIST

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users", description="Operations on users")


# create a user endpoint:
@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if UserModel.find_by_username(user_data["username"]):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**user_data)
        user.password = sha256.hash(user.password)

        try:
            user.save_to_db()
            return user, 201
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the user.")


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.find_by_username(user_data["username"])
        print(user)
        # sha256 verifies the password and returns True if it matches
        if user and sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"message": "Invalid credentials"}, 401


# get user by id endpoint
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        try:
            user = UserModel.find_by_id(user_id)
            return user
        except SQLAlchemyError:
            abort(500, message="An error occurred while retrieving the user.")

    # delete user endpoint:
    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        try:
            user.delete_from_db()
            return {"message": "User deleted."}
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the user.")


# logout endpoint:
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "User logged out."}, 200
