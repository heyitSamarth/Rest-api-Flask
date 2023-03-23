from flask.views import MethodView
from flask_smorest import Blueprint,abort #Divide api in multiple segments
from passlib.hash import pbkdf2_sha256
from Schemas import UserSchema
from models import UserModel
from db import db
from flask_jwt_extended import create_access_token,jwt_required,get_jwt

from blocklist import BLOCKLSIT

blp =Blueprint("users","Users",__name__,description="Operations on users")

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti=get_jwt()["jti"]
        BLOCKLSIT.add(jti)
        return {"message":"USer LOgged out"}
        


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(Self,user_data):
        if UserModel.query.filter(UserModel.username==user_data["username"]).first():
            abort(409,message="A user with that usewr name already exists")
        user=UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]))
        db.session.add(user)
        db.session.commit()

        return {"message":"user created Succesfully"},201
    
@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):

        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200

        abort(401, message="Invalid credentials.")