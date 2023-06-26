import json

from flask_jwt_extended import create_access_token


def test_rota_requer_professor(client, mysql_database, appauth):
    with appauth.app_context():
        test_user = {"id": 1, "username": "usuarioteste", "perfil": "admin"}
        access_token = create_access_token(identity=test_user)

    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.get('/adicionar_aluno', headers=headers)
    assert response.status_code == 200


def test_lista_alunos(client, mysql_database):
    response = client.get('/lista_aluno')
    assert response.status_code == 200

    mysql_database.cursor.execute('DELETE FROM alunos')
    response = client.get('/lista_aluno')
    assert response.status_code == 404


def test_adicionar_aluno(client, mysql_database):
    response = client.post(
        '/adicionar_aluno', data={'nome': 'Teste', 'idade': 20})
    assert response.status_code == 200

    response = client.post(
        '/adicionar_aluno', data={'nome': 'Teste', 'idade': -20})
    assert response.status_code == 400


def test_deletar_aluno1(client, mysql_database):
    mysql_database.cursor.execute(
        'INSERT INTO alunos (nome, idade) VALUES ("Teste", 20)')
    aluno_id = mysql_database.cursor.lastrowid

    response = client.get(f'/deletar_aluno/{aluno_id}')
    assert response.status_code == 200

    response = client.get('/deletar_aluno/999999')
    assert response.status_code == 404


def test_adicionar_aluno_json(client, mysql_database):
    data = {"name": "John", "age": 23}
    response = client.post(
        '/adicionar_aluno',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert b"Aluno adicionado com sucesso" in response.data


def test_editar_aluno_json(client, mysql_database):
    data = {"name": "John", "age": 24}
    response = client.post(
        '/editar_aluno/1',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert b"Aluno editado com sucesso" in response.data


def test_deletar_aluno2(client, mysql_database):
    response = client.get('/deletar_aluno/1')
    assert response.status_code == 200
    assert b"Aluno deletado com sucesso" in response.data


def test_adicionar_nota_json(client, mysql_database):
    data = {"nota": 9.5}
    response = client.post(
        '/adicionar_nota/1/1/1',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert b"Nota adicionada com sucesso" in response.data


def test_login(client, mysql_database):
    data = {"username": "test_user", "password": "test_password"}
    response = client.post(
        '/login', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert b"Login realizado com sucesso" in response.data


def test_registro_usuario1(client, mysql_database):
    data = {
            "username": "test_user",
            "password": "test_password",
            "email": "test@test.com"
            }

    response = client.post(
        '/registro_usuario',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert b"Registro realizado com sucesso" in response.data


def test_ver_notas(client, mysql_database):
    response = client.get('/ver_notas/test_user')
    assert response.status_code == 200
    notas = json.loads(response.data)
    assert notas == ["nota1", "nota2", "nota3"]


def test_atualizar_informacoes(client, mysql_database):
    data = {"nome": "Novo Nome", "email": "novo_email@test.com"}
    response = client.post(
        '/atualizar_informacoes/test_user',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert ("Informações atualizadas com sucesso".encode('utf-8')
            in response.data)


def test_registro_usuario2(client, mysql_database):
    data = {
            "username": "test_user",
            "password": "test_pass",
            "email": "test@test.com"
            }
    response = client.post(
        '/registro_usuario',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert b"Usuario registrado com sucesso" in response.data


def test_esqueci_senha(client, mysql_database):
    data = {"email": "test@test.com"}
    response = client.post(
        '/esqueci_senha',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert b"Email enviado com sucesso" in response.data


def test_deletar_aluno3(client, mysql_database):
    idAluno = 1
    response = client.get(f'/deletar_aluno/{idAluno}')
    assert response.status_code == 200
    assert b"Aluno deletado com sucesso" in response.data


def test_criar_avaliacao_grupo(client, mysql_database):
    idmateria = 1
    response = client.get(f'/criar_avaliacao_grupo/{idmateria}')
    assert response.status_code == 200
    assert "Avaliação criada com sucesso".encode('utf-8') in response.data
