from unittest.mock import MagicMock, Mock

import pytest

from connection.usuario import Usuario


@pytest.fixture
def mysql_mock():
    mysql_mock = MagicMock()
    cursor_mock = Mock()
    cursor_mock.fetchone.return_value = {"nome": "admin"}
    cursor_mock.fetchall.return_value = [
                                        {"nome": "admin"},
                                        {"nome": "professor"}
                                        ]
    mysql_mock.connection.cursor.return_value = cursor_mock
    return mysql_mock


@pytest.fixture
def user_instance(mysql_mock):
    return Usuario(mysql_mock)


def test_buscar_por_id(user_instance):
    result = user_instance.buscar_por_id(1)
    assert result['nome'] == 'admin'


def test_buscar_por_nome(user_instance):
    result = user_instance.buscar_por_nome('admin')
    assert len(result) == 1
    assert result[0]['nome'] == 'admin'


def test_editar(user_instance):
    user_instance.editar(1, {
                                "usuario": "admin",
                                "senha": "senha",
                                "email": "admin@example.com"
                                })
    user_instance.mysql.connection.commit.assert_called_once()


def test_apagar(user_instance):
    user_instance.apagar(1)
    user_instance.mysql.connection.commit.assert_called_once()


def test_aprovar_usuario(user_instance):
    user_instance.aprovar_usuario(1)
    user_instance.mysql.connection.commit.assert_called_once()


def test_get_total_usuarios(user_instance):
    (
        user_instance.mysql.connection.cursor.return_value
        .fetchone.return_value
    ) = [10]
    assert user_instance.get_total_usuarios() == 10


def test_get_total_avaliacoes_realizadas(user_instance):
    (
        user_instance.mysql.connection.cursor.return_value
        .fetchone.return_value
    ) = [5]
    assert user_instance.get_total_avaliacoes_realizadas() == 5


def test_login_nao_aprovado(user_instance):
    credentials = {"usuario": "admin", "senha": "senha"}
    result = user_instance.login_nao_aprovado(credentials)
    assert result['nome'] == 'admin'


def test_login(user_instance):
    credentials = {"usuario": "admin", "senha": "senha"}
    result = user_instance.login(credentials)
    assert result['nome'] == 'admin'


def test_editar_perfil(user_instance):
    user_instance.editar_perfil(1, 'admin')
    user_instance.mysql.connection.commit.assert_called_once()


def test_registro(user_instance):
    registroUsuario = {
                        "usuario": "admin",
                        "senha": "senha",
                        "email": "admin@example.com",
                        "nome": "Admin"
                        }
    assert len(user_instance.registro(registroUsuario)) == 7


def test_salvarSenha(user_instance):
    verificar = {"usuario": "admin", "codigo": "1234567", "password": "senha"}
    assert user_instance.salvarSenha(verificar)


def test_recuperar_senha(user_instance):
    email = "admin@example.com"
    assert len(user_instance.recuperar_senha(email)) == 7


def test_redefinir_senha(user_instance):
    assert user_instance.redefinir_senha(1, "admin@example.com", "nova_senha")


def test_buscar_usuarios_verificados(user_instance):
    result = user_instance.buscar_usuarios_verificados()
    assert len(result) == 2
    assert result[0]['nome'] == 'admin'
    assert result[1]['nome'] == 'professor'
