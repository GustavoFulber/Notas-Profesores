from unittest.mock import Mock

import pytest

from connection.notas_gerais import NotasGerais


@pytest.fixture
def notas_gerais():
    mysql_mock = Mock()
    notas = NotasGerais(mysql_mock)
    return notas


def test_listar_notas_gerais(notas_gerais):
    # Criar um mock para o retorno do fetchall
    (notas_gerais.mysql.connection.cursor()
     .fetchall.return_value) = [
                              {'id': 1, 'nome': 'nota 1'},
                              {'id': 2, 'nome': 'nota 2'}
                              ]

    result = notas_gerais.listar_notas_gerais()

    (notas_gerais.mysql.connection.cursor()
     .execute.assert_called_once_with)("SELECT * FROM notas_gerais")
    assert result == [
                     {'id': 1, 'nome': 'nota 1'},
                     {'id': 2, 'nome': 'nota 2'}
                     ]


def test_obter_notas_gerais_por_id(notas_gerais):
    (notas_gerais.mysql.connection.cursor()
     .fetchone.return_value) = {'id': 1, 'nome': 'nota 1'}

    result = notas_gerais.obter_notas_gerais_por_id(1)

    query = "SELECT * FROM notas_gerais WHERE idnotas_gerais = %s"
    (notas_gerais.mysql.connection.cursor()
     .execute.assert_called_once_with)(
                                       query, (1,)
                                      )
    assert result == {'id': 1, 'nome': 'nota 1'}


def test_inserir_notas_gerais(notas_gerais):
    notas = {
            'avalicao_objetiva': 90,
            'avaliacao_dissertativa': 85,
            'uas': 3,
            'entregas': 1,
            'idmateria': 1
            }
    notas_gerais.mysql.connection.cursor().lastrowid = 1

    result = notas_gerais.inserir_notas_gerais(notas)

    notas_gerais.mysql.connection.cursor().execute.assert_called_once_with(
        "INSERT INTO notas_gerais "
        "(avalicao_objetiva, avaliacao_dissertativa, "
        "uas, entregas, idmateria) VALUES (%s, %s, %s, %s, %s)",
        (90, 85, 3, 1, 1)
    )
    assert result == 1


def test_atualizar_notas_gerais(notas_gerais):
    notas = {
            'avalicao_objetiva': 90,
            'avaliacao_dissertativa': 85,
            'uas': 3,
            'entregas': 1
            }
    notas_gerais.mysql.connection.cursor().fetchone.return_value = [1]

    result = notas_gerais.atualizar_notas_gerais(1, notas)

    calls = notas_gerais.mysql.connection.cursor().execute.call_args_list
    print(calls)  # Para ver o que foi chamado

    query = ('UPDATE notas_gerais SET avalicao_objetiva = %s, \
              avaliacao_dissertativa = %s, uas = %s, entregas = %s\
              WHERE idnotas_gerais = %s')
    q2 = 'SELECT idAluno FROM aluno_notas_gerais WHERE idnotas_gerais = %s',

    assert any(
        call == (
            (
                q2, (1,),
            ),
        )
        for call in calls
    )
    assert any(
        call == (
            (
                query, (90, 85, 3, 1, 1),
            ),
        )
        for call in calls
    )
    assert result == 1


def test_idAluno_por_gerais(notas_gerais):
    notas_gerais.mysql.connection.cursor().fetchone.return_value = [1]

    result = notas_gerais.idAluno_por_gerais(1)

    calls = notas_gerais.mysql.connection.cursor().execute.call_args_list
    print(calls)  # Para ver o que foi chamado

    qury = 'SELECT idAluno FROM aluno_notas_gerais WHERE idnotas_gerais = %s'

    assert any(
                call == (
                        (
                            qury, (1,),
                        ),
                    )
                for call in calls
               )
    assert result == 1


def test_excluir_gerais(notas_gerais):
    notas_gerais.mysql.connection.cursor().fetchone.return_value = [1]

    result = notas_gerais.excluir_gerais(1)

    notas_gerais.mysql.connection.cursor().execute.assert_any_call(
        "SELECT idAluno FROM aluno_notas_gerais WHERE idnotas_gerais = %s",
        (1,)
    )
    notas_gerais.mysql.connection.cursor().execute.assert_any_call(
        "DELETE FROM aluno_notas_gerais WHERE idnotas_gerais = %s", (1,)
    )
    notas_gerais.mysql.connection.cursor().execute.assert_any_call(
        "DELETE FROM notas_gerais WHERE idnotas_gerais = %s", (1,)
    )
    assert result == 1


def test_excluir_notas_gerais(notas_gerais):
    notas_gerais.excluir_notas_gerais(1)

    notas_gerais.mysql.connection.cursor().execute.assert_called_once_with(
        "DELETE FROM notas_gerais WHERE idnotas_gerais = %s", (1,)
    )
