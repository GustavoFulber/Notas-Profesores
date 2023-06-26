from flask import request
from flask_jwt_extended import get_jwt_identity


def perfil():
    jwt_cookie_name = "access_token_cookie"
    if jwt_cookie_name not in request.cookies:
        return None

    user_identity = get_jwt_identity()
    if user_identity and "perfil" in user_identity:
        return user_identity["perfil"]
    return None


def custom_template_context():
    return {'user_perfil': perfil()}
