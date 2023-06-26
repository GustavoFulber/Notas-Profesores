from unittest.mock import MagicMock

import pytest

from connection.aluno_notas_gerais import AlunoNotasGerais


@pytest.fixture
def mysql():
    return MagicMock()


@pytest.fixture
def aluno_notas_gerais(mysql):
    return AlunoNotasGerais(mysql)


def test_buscar_todos(aluno_notas_gerais, mysql):
    cursor = MagicMock()
    mysql.connection.cursor.return_value = cursor
    cursor.fetchall.return_value = ['result']

    result = aluno_notas_gerais.buscar_todos()

    cursor.execute.assert_called_once_with('SELECT * FROM aluno_notas_gerais')
    assert result == ['result']


def test_buscar_por_id(aluno_notas_gerais, mysql):
    cursor = MagicMock()
    mysql.connection.cursor.return_value = cursor
    cursor.fetchone.return_value = ['result']

    result = aluno_notas_gerais.buscar_por_id(1)

    q = 'SELECT * FROM aluno_notas_gerais WHERE id=%s'
    cursor.execute.assert_called_once_with(q, (1,))
    assert result == ['result']


def test_buscar_por_idAluno(aluno_notas_gerais, mysql):
    cursor = MagicMock()
    mysql.connection.cursor.return_value = cursor
    cursor.fetchall.return_value = ['result']

    result = aluno_notas_gerais.buscar_por_idAluno(1)

    cursor.execute.assert_called_once()
    assert result == ['result']


def test_buscar_por_idAluno_materia(aluno_notas_gerais, mysql):
    cursor = MagicMock()
    mysql.connection.cursor.return_value = cursor
    cursor.fetchall.return_value = ['result']

    result = aluno_notas_gerais.buscar_por_idAluno_materia(1, 1)

    cursor.execute.assert_called_once()
    assert result == ['result']


def test_buscar_por_idAluno_comid(aluno_notas_gerais, mysql):
    cursor = MagicMock()
    mysql.connection.cursor.return_value = cursor
    cursor.fetchall.return_value = ['result']

    result = aluno_notas_gerais.buscar_por_idAluno_comid(1, 1)

    cursor.execute.assert_called_once()
    assert result == ['result']


def test_criar(aluno_notas_gerais, mysql):
    cursor = MagicMock()
    mysql.connection.cursor.return_value = cursor
    cursor.lastrowid = 1

    aluno_notas_gerais_data = {'idAluno': 1, 'idnotas_gerais': 1}
    result = aluno_notas_gerais.criar(aluno_notas_gerais_data)

    q = "INSERT INTO aluno_notas_gerais(idAluno, idnotas_gerais)VALUES(%s, %s)"
    cursor.execute.assert_called_once_with(q,  (1, 1))
    assert result == 1


def test_editar(aluno_notas_gerais, mysql):
    cursor = MagicMock()
    mysql.connection.cursor.return_value = cursor

    aluno_notas_gerais_data = {'idAluno': 1, 'idnotas_gerais': 1}
    aluno_notas_gerais.editar(1, aluno_notas_gerais_data)

    q = "UPDATE aluno_notas_gerais SET idAluno=%s, ",
    cursor.execute.assert_called_once_with(
                                            q +
                                            "idnotas_gerais=%s WHERE id=%s",
                                            (1, 1, 1))


def test_apagar(aluno_notas_gerais, mysql):
    cursor = MagicMock()
    mysql.connection.cursor.return_value = cursor

    aluno_notas_gerais.apagar(1)

    cursor.execute.assert_called_once_with(
        'DELETE FROM aluno_notas_gerais WHERE id=%s', (1,))


def test_apagar_aluno_id(aluno_notas_gerais, mysql):
    cursor = MagicMock()
    mysql.connection.cursor.return_value = cursor

    aluno_notas_gerais.apagar_aluno_id(1)

    cursor.execute.assert_called_once()


def test_verificarNotaVazia(aluno_notas_gerais):
    class MockForm:
        def __init__(self):
            self.form = {'avaliacao_objetiva': '  ',
                         'avaliacao_dissertativa': '  ',
                         'uas': '  ',
                         'entregas': '  '}

    notas = MockForm()
    result = aluno_notas_gerais.verificarNotaVazia(notas)
    assert not result


def test_verificarNotaMaiorQueDez(aluno_notas_gerais):
    class MockForm:
        def __init__(self):
            self.form = {'avaliacao_objetiva': '11',
                         'avaliacao_dissertativa': '10',
                         'uas': '10',
                         'entregas': '10'}

    notas = MockForm()
    result = aluno_notas_gerais.verificarNotaMaiorQueDez(notas)
    assert not result
