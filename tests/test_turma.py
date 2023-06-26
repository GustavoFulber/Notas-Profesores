from unittest.mock import MagicMock

import pytest

from connection.turma import Turma


@pytest.fixture
def mysql_mock():
    return MagicMock()


def test_buscar_todos(mysql_mock):
    turma = Turma(mysql_mock)

    # Defina o comportamento esperado para o mock
    (mysql_mock.connection.cursor()
     .fetchone.return_value) = [('Turma A', '2023-01'), ('Turma B', '2023-02')]

    # Chame o método a ser testado
    resultado = turma.buscar_todos()

    # Verifique o resultado
    assert resultado == [('Turma A', '2023-01'), ('Turma B', '2023-02')]


def test_vincular_aluno(mysql_mock):
    turma = Turma(mysql_mock)

    # Chame o método a ser testado
    turma.vincular_aluno(1, 10)

    # Verifique se os métodos corretos foram chamados
    cursor_mock = mysql_mock.connection.cursor()
    cursor_mock.execute.assert_called_once_with(
        "INSERT INTO turma_aluno (idturma, idaluno) VALUES (%s, %s)", (1, 10))
    mysql_mock.connection.commit.assert_called_once()
    cursor_mock.close.assert_called_once()


def test_remover_aluno(mysql_mock):
    turma = Turma(mysql_mock)

    # Chame o método a ser testado
    turma.remover_aluno(1, 10)

    # Verifique se os métodos corretos foram chamados
    mysql_mock.connection.cursor().execute.assert_called_once_with(
        "DELETE FROM turma_aluno WHERE idturma=%s AND idaluno=%s", (1, 10))
    mysql_mock.connection.commit.assert_called_once()


def test_listar_alunos_nao_vinculados(mysql_mock):
    turma = Turma(mysql_mock)

    # Defina o comportamento esperado para o mock
    (mysql_mock.connection.cursor()
     .fetchone.return_value) = [('Aluno A', '2023-01'), ('Aluno B', '2023-02')]

    # Chame o método a ser testado
    resultado = turma.listar_alunos_nao_vinculados(1)

    # Verifique o resultado
    assert resultado == [('Aluno A', '2023-01'), ('Aluno B', '2023-02')]


def test_listar_alunos_vinculados(mysql_mock):
    turma = Turma(mysql_mock)

    # Defina o comportamento esperado para o mock
    (mysql_mock.connection.cursor()
     .fetchone.return_value) = [('Aluno A', '2023-01'), ('Aluno B', '2023-02')]

    # Chame o método a ser testado
    resultado = turma.listar_alunos_vinculados(1)

    # Verifique o resultado
    assert resultado == [('Aluno A', '2023-01'), ('Aluno B', '2023-02')]


def test_buscar_por_id(mysql_mock):
    turma = Turma(mysql_mock)

    # Defina o comportamento esperado para o mock
    (mysql_mock.connection.cursor()
     .fetchone.return_value) = ('Turma A', '2023-01')

    # Chame o método a ser testado
    resultado = turma.buscar_por_id(1)

    # Verifique o resultado
    assert resultado == ('Turma A', '2023-01')


def test_adicionar_turma(mysql_mock):
    turma = Turma(mysql_mock)

    # Chame o método a ser testado
    turma.adicionar_turma('Turma A', '2023-01')

    # Verifique se os métodos corretos foram chamados
    mysql_mock.connection.cursor().execute.assert_called_once_with(
        "INSERT INTO turma (nome, periodo) VALUES (%s, %s)",
        ('Turma A', '2023-01'))
    mysql_mock.connection.commit.assert_called_once()


def test_editar_turma(mysql_mock):
    turma = Turma(mysql_mock)

    # Chame o método a ser testado
    turma.editar_turma(1, 'Turma B', '2023-02')

    # Verifique se os métodos corretos foram chamados
    mysql_mock.connection.cursor().execute.assert_called_once_with(
        "UPDATE turma SET nome=%s, periodo=%s WHERE idturma=%s",
        ('Turma B', '2023-02', 1))
    mysql_mock.connection.commit.assert_called_once()


def test_deletar_turma(mysql_mock):
    turma = Turma(mysql_mock)

    # Chame o método a ser testado
    turma.deletar_turma(1)

    # Verifique se os métodos corretos foram chamados
    cursor_mock = mysql_mock.connection.cursor()
    cursor_mock.execute.assert_any_call(
        "DELETE aluno_notas_gerais FROM aluno_notas_gerais JOIN"
        " notas_gerais ON aluno_notas_gerais.idnotas_gerais ="
        " notas_gerais.idnotas_gerais JOIN materia ON"
        " notas_gerais.idmateria = materia.id WHERE materia.idturma = %s",
        (1,))
    cursor_mock.execute.assert_any_call(
        "DELETE notas_gerais FROM notas_gerais JOIN materia ON"
        " notas_gerais.idmateria = materia.id WHERE materia.idturma = %s",
        (1,))
    cursor_mock.execute.assert_any_call(
        "DELETE grupo_aluno FROM grupo_aluno JOIN grupo ON"
        " grupo_aluno.idgrupo = grupo.idgrupo JOIN materia ON"
        " grupo.idmateria = materia.id WHERE materia.idturma = %s",
        (1,))
    cursor_mock.execute.assert_any_call(
        "DELETE grupo FROM grupo JOIN materia ON grupo.idmateria"
        " = materia.id WHERE materia.idturma = %s",
        (1,))
    cursor_mock.execute.assert_any_call(
        "DELETE aluno_avaliacao_360 FROM aluno_avaliacao_360 JOIN"
        " avaliacao_360 ON aluno_avaliacao_360.idavaliacao_360"
        " = avaliacao_360.idavaliacao_360 JOIN materia ON"
        " avaliacao_360.idmateria = materia.id WHERE materia.idturma = %s",
        (1,))
    cursor_mock.execute.assert_any_call(
        "DELETE avaliacao_360 FROM avaliacao_360 JOIN materia ON"
        " avaliacao_360.idmateria = materia.id WHERE materia.idturma = %s",
        (1,))
    (cursor_mock.
     execute.assert_any_call
     )("DELETE FROM turma_aluno WHERE idturma = %s", (1,))
    (cursor_mock.
     execute.assert_any_call
     )("DELETE FROM materia WHERE idturma = %s", (1,))
    (cursor_mock.
     execute.assert_any_call
     )("DELETE FROM turma WHERE idturma = %s", (1,))
    mysql_mock.connection.commit.assert_called_once()
    cursor_mock.close.assert_called_once()
