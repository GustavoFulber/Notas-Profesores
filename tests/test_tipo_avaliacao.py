from unittest.mock import MagicMock, Mock

import pytest

from connection.tipo_avaliacao import TipoAvaliacao


@pytest.fixture
def mock_mysql():
    mysql = MagicMock()
    mysql.connection.cursor.return_value = Mock()
    return mysql


def test_buscar_todos(mock_mysql):
    tipo_avaliacao = TipoAvaliacao(mock_mysql)
    tipo_avaliacao.buscar_todos()
    (mock_mysql.connection.cursor().
     execute.assert_called_with("SELECT * FROM tipo_avaliacao"))


def test_buscar_por_id(mock_mysql):
    tipo_avaliacao = TipoAvaliacao(mock_mysql)
    tipo_avaliacao.buscar_por_id(1)
    mock_mysql.connection.cursor().execute.assert_called_with(
        "SELECT * FROM tipo_avaliacao WHERE idtipo_avaliacao = %s", (1,))


def test_salvar(mock_mysql):
    tipo_avaliacao = TipoAvaliacao(mock_mysql)
    tipo_avaliacao.salvar("nome")
    mock_mysql.connection.cursor().execute.assert_called_with(
        "INSERT INTO tipo_avaliacao (nome) VALUES (%s)", ("nome",))
    mock_mysql.connection.commit.assert_called()


def test_editar(mock_mysql):
    tipo_avaliacao = TipoAvaliacao(mock_mysql)
    tipo_avaliacao.editar(1, "nome")
    mock_mysql.connection.cursor().execute.assert_called_with(
        "UPDATE tipo_avaliacao SET nome = %s WHERE idtipo_avaliacao = %s",
        ("nome", 1))
    mock_mysql.connection.commit.assert_called()


def test_apagar(mock_mysql):
    tipo_avaliacao = TipoAvaliacao(mock_mysql)
    tipo_avaliacao.apagar(1)
    mock_mysql.connection.cursor().execute.assert_called_with(
        "DELETE FROM tipo_avaliacao WHERE idtipo_avaliacao = %s", (1,))
    mock_mysql.connection.commit.assert_called()
