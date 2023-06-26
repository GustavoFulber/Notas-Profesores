from unittest.mock import MagicMock

import pytest

from connection.materia import Materia


@pytest.fixture
def mock_mysql():
    mock = MagicMock()
    mock.connection.cursor.return_value.fetchall.return_value = []
    return mock


@pytest.fixture
def materia(mock_mysql):
    return Materia(mock_mysql)


def test_buscar_todas(materia, mock_mysql):
    admin_sql = """
        SELECT m.id, m.nome, u.nome, t.periodo,
                (SELECT COUNT(*) FROM avaliacao WHERE idmateria =
                 m.id AND idaluno_avaliado != idaluno_realizando
                 ) as avaliacoes_criadas,
                (SELECT COUNT(*) FROM avaliacao WHERE idmateria =
                 m.id AND completo = TRUE AND idaluno_avaliado !=
                  idaluno_realizando) as avaliacoes_realizadas,
                (SELECT COUNT(*) FROM avaliacao WHERE idmateria = m.id AND
                 idaluno_avaliado = idaluno_realizando) as
                  auto_avaliacoes_criadas,
                (SELECT COUNT(*) FROM avaliacao WHERE idmateria = m.id AND
                 idaluno_avaliado = idaluno_realizando AND completo = TRUE)
                  as auto_avaliacoes_realizadas
                FROM materia m
                JOIN usuario u ON m.idresponsavel = u.idusuario
                JOIN turma t ON m.idturma = t.idturma
    """
    user_sql = """
        SELECT m.id, m.nome, u.nome, t.periodo,
                (SELECT COUNT(*) FROM avaliacao WHERE idmateria = m.id AND
                 idaluno_avaliado != idaluno_realizando) as avaliacoes_criadas,
                (SELECT COUNT(*) FROM avaliacao WHERE idmateria = m.id AND
                 completo = TRUE AND idaluno_avaliado != idaluno_realizando)
                  as avaliacoes_realizadas,
                (SELECT COUNT(*) FROM avaliacao WHERE idmateria = m.id AND
                 idaluno_avaliado = idaluno_realizando) as
                  auto_avaliacoes_criadas,
                (SELECT COUNT(*) FROM avaliacao WHERE idmateria = m.id AND
                 idaluno_avaliado = idaluno_realizando AND completo = TRUE)
                  as auto_avaliacoes_realizadas
                FROM materia m
                JOIN usuario u ON m.idresponsavel = u.idusuario
                JOIN turma t ON m.idturma = t.idturma
                WHERE m.idresponsavel = %s
    """

    # Teste para perfil admin
    materia.buscar_todas(1, 'admin')
    assert mock_mysql.connection.cursor.called
    assert (mock_mysql.connection.cursor.return_value.execute
            .called_with)(admin_sql)

    # Teste para perfil não-admin
    materia.buscar_todas(1, 'user')
    assert (mock_mysql.connection.cursor.return_value
            .execute.called_with)(user_sql, (1,))


def test_buscar_materias_por_usuario(materia, mock_mysql):
    user_sql = """
        SELECT DISTINCT m.id, m.nome
                        FROM materia m
                        JOIN notas_gerais ng ON ng.idmateria = m.id
                        JOIN aluno_notas_gerais ang ON ang.idnotas_gerais =
                         ng.idnotas_gerais
                        JOIN aluno a ON a.idaluno = ang.idaluno
                        WHERE a.idusuario = %s
                        UNION
                        SELECT DISTINCT m.id, m.nome
                        FROM materia m
                        JOIN avaliacao_360 av ON av.idmateria = m.id
                        JOIN aluno_avaliacao_360 aav ON aav.idavaliacao_360 =
                         av.idavaliacao_360
                        JOIN aluno a ON a.idaluno = aav.idaluno
                        WHERE a.idusuario = %s
    """

    materia.buscar_materias_por_usuario(1)
    assert mock_mysql.connection.cursor.called
    assert (mock_mysql.connection.cursor.return_value
            .execute.called_with)(user_sql, (1, 1))


def test_buscar_por_id(materia, mock_mysql):
    materia.buscar_por_id(1)
    assert mock_mysql.connection.cursor.called
    assert (mock_mysql.connection.cursor.return_value
           .execute.called_with)("SELECT * FROM materia WHERE id = %s", (1,))


def test_adicionar_materia(materia, mock_mysql):
    materia.adicionar_materia("matematica", 1, 1)
    assert mock_mysql.connection.cursor.called
    assert (mock_mysql.connection.cursor.return_value
            .execute.called_with)("INSERT INTO materia (nome, idresponsavel, "
                                  "idturma) VALUES (%s, %s, %s)",
                                  ("matematica", 1, 1))


def test_editar_materia(materia, mock_mysql):
    materia.editar_materia(1, "fisica", 2, 2)
    assert mock_mysql.connection.cursor.called
    assert (mock_mysql.connection.cursor.return_value.
            execute.called_with)("UPDATE materia SET nome = %s, idresponsavel "
                                 "= %s, idturma = %s WHERE id = %s",
                                 ("fisica", 2, 2, 1))


def test_deletar_materia(materia, mock_mysql):
    materia.deletar_materia(1)
    assert mock_mysql.connection.cursor.called
    assert mock_mysql.connection.cursor.return_value.execute.call_count == 8
