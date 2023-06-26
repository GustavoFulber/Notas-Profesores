from unittest.mock import MagicMock

import pytest

from connection.avaliacao_360 import Avaliacao360


@pytest.fixture
def mysql_mock():
    mysql = MagicMock()
    mysql.connection.cursor.return_value = MagicMock()
    return mysql


def test_salvar_avaliacao(mysql_mock):
    avaliacao = Avaliacao360(mysql_mock)
    example_avaliacao = {
        'comunicacao': 5,
        'cognitivo': 5,
        'autogestao': 5,
        'autonomia': 5,
        'protagonismo': 5,
        'interacao': 5,
        'idtipo_avaliacao': 1,
        'idmateria': 1,
    }
    idavaliacao = avaliacao.salvar(example_avaliacao)
    mysql_mock.connection.cursor.return_value.execute.assert_called()
    mysql_mock.connection.commit.assert_called()
    assert idavaliacao is not None  # o valor exato depende da sua implementaçã


def test_buscar_por_id(mysql_mock):
    avaliacao = Avaliacao360(mysql_mock)
    idavaliacao_360 = 1
    result = avaliacao.buscar_por_id(idavaliacao_360)
    q = "SELECT * FROM avaliacao_360 WHERE idavaliacao_360 = %s"
    (mysql_mock.connection.cursor.return_value
     .execute.assert_called_with)(q, (idavaliacao_360,))
    assert result is not None  # o valor exato depende da sua implementação


def test_buscar_todos(mysql_mock):
    avaliacao = Avaliacao360(mysql_mock)
    result = avaliacao.buscar_todos()
    (mysql_mock.connection.cursor.return_value.execute.
     assert_called_with)("SELECT * FROM avaliacao_360")
    assert result is not None  # o valor exato depende da sua implementação


def test_editar(mysql_mock):
    avaliacao = Avaliacao360(mysql_mock)
    idavaliacao_360 = 1
    example_avaliacao = {
        'comunicacao': 5,
        'cognitivo': 5,
        'autogestao': 5,
        'autonomia': 5,
        'protagonismo': 5,
        'interacao': 5,
        'idtipo_avaliacao': 1,
    }
    aluno_id = avaliacao.editar(idavaliacao_360, example_avaliacao)
    mysql_mock.connection.cursor.return_value.execute.assert_called()
    mysql_mock.connection.commit.assert_called()
    assert aluno_id is not None  # o valor exato depende da sua implementação


def test_excluir_avaliacao360(mysql_mock):
    avaliacao = Avaliacao360(mysql_mock)
    idavaliacao_360 = 1
    aluno_id = avaliacao.excluir_avaliacao360(idavaliacao_360)
    mysql_mock.connection.cursor.return_value.execute.assert_called()
    mysql_mock.connection.commit.assert_called()
    assert aluno_id is not None


def test_idAluno_por_360(mysql_mock):
    avaliacao = Avaliacao360(mysql_mock)
    idavaliacao_360 = 1
    aluno_id = avaliacao.idAluno_por_360(idavaliacao_360)
    q = "SELECT idAluno FROM aluno_avaliacao_360 WHERE idavaliacao_360 = %s"
    (mysql_mock.connection.cursor.return_value.execute
     .assert_called_with)(q, (idavaliacao_360,))
    assert aluno_id is not None  # o valor exato depende da sua implementação


def test_apagar(mysql_mock):
    avaliacao = Avaliacao360(mysql_mock)
    idavaliacao_360 = 1
    avaliacao.apagar(idavaliacao_360)
    q = "DELETE FROM avaliacao_360 WHERE idavaliacao_360 = %s"
    (mysql_mock.connection.cursor.return_value.execute
     .assert_called_with)(q, (idavaliacao_360,))
    mysql_mock.connection.commit.assert_called()
