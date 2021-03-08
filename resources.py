from typing import Union
from flask_restful import Resource, reqparse

from models import User
from database import db_session 

def validate_name(value:str, name:str) -> Union[ValueError, str]:
    user:User = User.query.filter(User.name == value).first()
    if user:
        raise ValueError(f"El usuario con el {name} {value} ya existe, por favor utilice otro")
    return value

def validation_email(value:str, name:str) -> Union[ValueError, str]:
    if "@" not in value:
        raise ValueError(f"El parametro {name} no es un email, usted nos dio {value}")
    return value

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('name', type=validate_name, location="form", required=True)
parser.add_argument('email', type=validation_email, location="form", required=True)

class UserResource(Resource):
    def get(self):
        users = User.query.all()
        return dict(users=[dict(name=user.name, email=user.email) for user in users] if users else [])

    def post(self):
        args = parser.parse_args()
        name = args.get("name")
        email = args.get("email")
        user = User.query.filter(User.name == name).first()
        if user:
            return dict()
        user = User(name=name, email=email)
        db_session.add(user)
        db_session.commit()
        return dict(name=user.name, email=user.email)