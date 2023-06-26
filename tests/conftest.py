import os

import MySQLdb
import pytest
import sqlparse
from flask import Flask


@pytest.fixture(scope='module')
def app():
    from app import app
    yield app


@pytest.fixture(scope='module')
def client(app):
    return app.test_client()


@pytest.fixture(scope='module')
def mysql_database():
    # Criar o banco de dados de teste
    db = MySQLdb.connect(host="127.0.0.2", user="root", passwd="100%Tabajara")
    cursor = db.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS calculanotas')
    db.commit()

    # Executar as migrações
    migration_files = os.listdir('venv_tests/dbmigrations')
    migration_files.sort()
    for file in migration_files:
        if file.endswith('.sql'):
            with open(f'venv_tests/dbmigrations/{file}') as f:
                sql_commands = sqlparse.split(f.read())
                for command in sql_commands:
                    if command:
                        cursor.execute(command)
                        db.commit()

    yield
    db.close()


@pytest.fixture(scope='module')
def appauth():
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = '127.0.0.2'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '100%Tabajara'
    app.config['MYSQL_DB'] = 'calculanota'
    app.config['JWT_SECRET_KEY'] = 'sua-chave-secreta-aqui'
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    return app


@pytest.fixture(scope='module')
def client_test(appauth):
    return appauth.test_client()
