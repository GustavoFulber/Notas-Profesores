from unittest.mock import MagicMock

from connection.aluno_avaliacao_360 import AlunoAvaliacao360


def test_salvar():
    # Criação do objeto MySQL simulado (mocked)
    mock_mysql = MagicMock()
    mock_cursor = MagicMock()
    mock_mysql.connection.cursor.return_value = mock_cursor

    # Instanciando a classe a ser testada
    aluno_avaliacao = AlunoAvaliacao360(mock_mysql)

    # Valores a serem passados para o método
    aluno_avaliacao_dict = {"idAluno": 1, "idavaliacao_360": 1}

    # Executando o método
    aluno_avaliacao.salvar(aluno_avaliacao_dict)

    # Verificando se o método execute foi chamado corretamente
    q = "INSERT INTO aluno_avaliacao_360(idAluno,idavaliacao_360)VALUES(%s,%s)"
    mock_cursor.execute.assert_called_with(q, (1, 1))

    # Verificando se o método commit foi chamado
    mock_mysql.connection.commit.assert_called_once()


def test_editar():
    mock_mysql = MagicMock()
    mock_cursor = MagicMock()
    mock_mysql.connection.cursor.return_value = mock_cursor
    aluno_avaliacao = AlunoAvaliacao360(mock_mysql)
    aluno_avaliacao_dict = {"id": 1, "idAluno": 1, "idavaliacao_360": 1}
    aluno_avaliacao.editar(aluno_avaliacao_dict)
    q = "UPDATE aluno_avaliacao_360 SET idAluno=%s,idavaliacao_360=%s "
    mock_cursor.execute.assert_called_with(q + "WHERE id=%s", (1, 1, 1))
    mock_mysql.connection.commit.assert_called_once()


def test_apagar():
    mock_mysql = MagicMock()
    mock_cursor = MagicMock()
    mock_mysql.connection.cursor.return_value = mock_cursor
    aluno_avaliacao = AlunoAvaliacao360(mock_mysql)
    aluno_avaliacao.apagar(1)
    q = "DELETE FROM aluno_avaliacao_360 WHERE id=%s"
    mock_cursor.execute.assert_called_with(q, (1,))
    mock_mysql.connection.commit.assert_called_once()


def test_apagar_aluno_id():
    mock_mysql = MagicMock()
    mock_cursor = MagicMock()
    mock_mysql.connection.cursor.return_value = mock_cursor
    aluno_avaliacao = AlunoAvaliacao360(mock_mysql)
    aluno_avaliacao.apagar_aluno_id(1)
    mock_cursor.execute.assert_called_with(
        "DELETE FROM aluno_avaliacao_360 WHERE idAluno = %s; DELETE "
        "FROM avaliacao_360 WHERE idavaliacao_360 IN ("
        "SELECT idavaliacao_360 FROM aluno_avaliacao_360 WHERE idAluno = %s);",
        (1, 1))
    mock_mysql.connection.commit.assert_called_once()


def test_buscar_por_id():
    mock_mysql = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1, 1, 1)
    mock_mysql.connection.cursor.return_value = mock_cursor
    aluno_avaliacao = AlunoAvaliacao360(mock_mysql)
    result = aluno_avaliacao.buscar_por_id(1)
    q = "SELECT * FROM aluno_avaliacao_360 WHERE id=%s"
    mock_cursor.execute.assert_called_with(q, (1,))
    assert result == {"id": 1, "idAluno": 1, "idavaliacao_360": 1}


def test_buscar_por_idaluno():
    mock_mysql = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(1, 1, 1), (2, 1, 2)]
    mock_mysql.connection.cursor.return_value = mock_cursor
    aluno_avaliacao = AlunoAvaliacao360(mock_mysql)
    result = aluno_avaliacao.buscar_por_idAluno(1)
    q = "SELECT * FROM aluno_avaliacao_360 WHERE idAluno=%s"
    mock_cursor.execute.assert_called_with(q, (1,))

    # Convertendo a saída de fetchall() em uma lista de dicionários
    result = [{
               "id": item[0],
               "idAluno": item[1],
               "idavaliacao_360": item[2]
               } for item in result]

    assert result == [
        {"id": 1, "idAluno": 1, "idavaliacao_360": 1},
        {"id": 2, "idAluno": 1, "idavaliacao_360": 2}
    ]


def test_buscar_todos():
    mock_mysql = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(1, 1, 1), (2, 1, 2), (3, 2, 1)]
    mock_mysql.connection.cursor.return_value = mock_cursor
    aluno_avaliacao = AlunoAvaliacao360(mock_mysql)
    result = aluno_avaliacao.buscar_todos()
    mock_cursor.execute.assert_called_with("SELECT * FROM aluno_avaliacao_360")
    assert result == [
        {"id": 1, "idAluno": 1, "idavaliacao_360": 1},
        {"id": 2, "idAluno": 1, "idavaliacao_360": 2},
        {"id": 3, "idAluno": 2, "idavaliacao_360": 1}
    ]


def test_buscar_por_idAluno_materia():
    mock_mysql = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {
                                        "idAluno": 1,
                                        "materia": 'Matemática',
                                        "nota": 8.5
                                        }
    mock_mysql.connection.cursor.return_value = mock_cursor

    aluno_avaliacao = AlunoAvaliacao360(mock_mysql)
    result = aluno_avaliacao.buscar_por_idAluno_materia(1, 'Matemática')

    q = "SELECT * FROM aluno_avaliacao_360 WHERE idAluno=%s AND materia=%s"
    mock_cursor.execute.assert_called_with(q, (1, 'Matemática'))
    assert result == mock_cursor.fetchone()


def test_atualizar_completo():
    mock_mysql = MagicMock()
    mock_cursor = MagicMock()
    mock_mysql.connection.cursor.return_value = mock_cursor

    aluno_avaliacao = AlunoAvaliacao360(mock_mysql)
    aluno_avaliacao_dict = {"idAluno": 1, "materia": 'Matemática', "nota": 9.5}

    aluno_avaliacao.atualizar_completo(aluno_avaliacao_dict)

    q = "UPDATE aluno_avaliacao_360 SET materia=%s, nota=%s WHERE idAluno=%s"
    mock_cursor.execute.assert_called_with(q, ('Matemática', 9.5, 1))
    mock_mysql.connection.commit.assert_called_once()


def test_buscar_por_id_ul():
    mock_mysql = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {
                                        "idAluno": 1,
                                        "materia": 'Matemática',
                                        "nota": 8.5
                                        }
    mock_mysql.connection.cursor.return_value = mock_cursor

    aluno_avaliacao = AlunoAvaliacao360(mock_mysql)
    result = aluno_avaliacao.buscar_por_id_ul(1)
    q = "SELECT * FROM aluno_avaliacao_360 WHERE id=%s ORDER BY id DESC "
    mock_cursor.execute.assert_called_with(q + "LIMIT 1", (1,))
    assert result == mock_cursor.fetchone()


def test_buscar_por_idAluno_comid():
    mock_mysql = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {
                                        "idAluno": 1,
                                        "id": 2,
                                        "materia": 'Matemática',
                                        "nota": 8.5
                                        }
    mock_mysql.connection.cursor.return_value = mock_cursor

    aluno_avaliacao = AlunoAvaliacao360(mock_mysql)
    result = aluno_avaliacao.buscar_por_idAluno_comid(1, 2)

    q = "SELECT * FROM aluno_avaliacao_360 WHERE idAluno=%s AND id=%s"
    mock_cursor.execute.assert_called_with(q, (1, 2))
    assert result == mock_cursor.fetchone()
