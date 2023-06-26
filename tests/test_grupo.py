from unittest.mock import MagicMock

from connection.grupo import Grupo


def test_buscar_por_materia():
    mock_mysql = MagicMock()
    mock_cursor = MagicMock()
    mock_mysql.connection.cursor.return_value = mock_cursor
    grupo = Grupo(mock_mysql)
    grupo.buscar_por_materia(1)

    q = "SELECT * FROM grupo WHERE idmateria = %s"
    mock_cursor.execute.assert_called_once_with(q, (1,))
    assert mock_cursor.fetchall.call_count == 1
    assert mock_cursor.close.call_count == 1


def test_buscar_por_id():
    mock_mysql = MagicMock()
    mock_cursor = MagicMock()
    mock_mysql.connection.cursor.return_value = mock_cursor
    grupo = Grupo(mock_mysql)
    grupo.buscar_por_id(1)

    q = "SELECT * FROM grupo WHERE idgrupo = %s"
    mock_cursor.execute.assert_called_once_with(q, (1,))
    assert mock_cursor.fetchone.call_count == 1
    assert mock_cursor.close.call_count == 1


def test_adicionar_grupo():
    mock_mysql = MagicMock()
    mock_cursor = MagicMock()
    mock_mysql.connection.cursor.return_value = mock_cursor
    grupo = Grupo(mock_mysql)
    grupo.adicionar_grupo('Nome', 1)

    q = "INSERT INTO grupo (nome, idmateria) VALUES (%s, %s)"
    mock_cursor.execute.assert_called_once_with(q, ('Nome', 1))
    assert mock_mysql.connection.commit.call_count == 1
    assert mock_cursor.close.call_count == 1


def test_editar_grupo():
    mock_mysql = MagicMock()
    mock_cursor = MagicMock()
    mock_mysql.connection.cursor.return_value = mock_cursor
    grupo = Grupo(mock_mysql)
    grupo.editar_grupo(1, 'Novo Nome')

    q = "UPDATE grupo SET nome = %s WHERE idgrupo = %s"
    mock_cursor.execute.assert_called_once_with(q, ('Novo Nome', 1))
    assert mock_mysql.connection.commit.call_count == 1
    assert mock_cursor.close.call_count == 1


def test_deletar_grupo():
    mock_mysql = MagicMock()
    mock_cursor = MagicMock()
    mock_mysql.connection.cursor.return_value = mock_cursor
    grupo = Grupo(mock_mysql)
    grupo.deletar_grupo(1)

    q = "DELETE FROM grupo WHERE idgrupo = %s"
    mock_cursor.execute.assert_called_once_with(q, (1,))
    assert mock_mysql.connection.commit.call_count == 1
    assert mock_cursor.close.call_count == 1


def test_vincular_aluno():
    mock_db = MagicMock()
    mock_cursor = MagicMock()

    mock_db.connection.cursor.return_value = mock_cursor
    grupo = Grupo(mock_db)

    grupo.vincular_aluno(1, 2)
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO grupo_aluno (idgrupo, idaluno) VALUES (%s, %s)", (1, 2))
    mock_db.connection.commit.assert_called_once()
    mock_cursor.close.assert_called_once()


def test_remover_aluno():
    mock_db = MagicMock()
    mock_cursor = MagicMock()

    mock_db.connection.cursor.return_value = mock_cursor
    grupo = Grupo(mock_db)

    grupo.remover_aluno(1, 2)
    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM grupo_aluno WHERE idgrupo=%s AND idaluno=%s", (1, 2))
    mock_db.connection.commit.assert_called_once()
    mock_cursor.close.assert_called_once()


def test_listar_alunos_nao_vinculados():
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{'idaluno': 1, 'nome': 'John'}]

    mock_db.connection.cursor.return_value = mock_cursor
    grupo = Grupo(mock_db)

    alunos = grupo.listar_alunos_nao_vinculados(1, 2)

    assert alunos == [{'idaluno': 1, 'nome': 'John'}]
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()


def test_listar_alunos_vinculados():
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{'idaluno': 1, 'nome': 'John'}]

    mock_db.connection.cursor.return_value = mock_cursor
    grupo = Grupo(mock_db)

    alunos = grupo.listar_alunos_vinculados(1)

    assert alunos == [{'idaluno': 1, 'nome': 'John'}]
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
