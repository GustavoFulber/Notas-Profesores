from unittest.mock import patch

import pytest
from flask import Flask
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required,
                                set_access_cookies)

from utils.perfil import custom_template_context, perfil

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secretona'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
jwt = JWTManager(app)


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return perfil()


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_perfil_no_cookie(client):
    with app.app_context():
        client.get('/')
        assert perfil()


def test_perfil_with_cookie_no_perfil(client):
    with app.app_context():
        test_user = {"id": 1, "username": "usuarioteste"}
        access_token = create_access_token(identity=test_user)
        resp = client.get('/')
        set_access_cookies(resp, access_token)
        assert perfil()


def test_perfil_with_cookie_with_perfil(client):
    with app.app_context():
        test_user = {"id": 1, "username": "usuarioteste", "perfil": "user"}
        access_token = create_access_token(identity=test_user)
        client.set_cookie(
                        'access_token_cookie', access_token, domain='localhost'
                        )
        resp = client.get('/protected')
        assert resp.data.decode() == "user"


def test_custom_template_context_no_perfil(client):
    with app.app_context():
        client.get('/')
        assert custom_template_context() == {'user_perfil': None}


@patch('utils.perfil.perfil', return_value="user")
def test_custom_template_context_with_perfil(mock_perfil, client):
    with app.app_context():
        client.get('/')
        assert custom_template_context() == {'user_perfil': "user"}
