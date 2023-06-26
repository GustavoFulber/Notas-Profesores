from unittest.mock import MagicMock

import pytest

from connection.aluno_materia import AlunoMateria


class TestAlunoMateria:
    @pytest.fixture
    def mysql_mock(self):
        mysql_mock = MagicMock()
        cursor_mock = MagicMock()
        mysql_mock.connection.cursor.return_value = cursor_mock
        return mysql_mock

    @pytest.fixture
    def aluno_materia(self, mysql_mock):
        return AlunoMateria(mysql_mock)

    def test_salvar(self, aluno_materia, mysql_mock):
        al = {"idAluno": 1, "idMateria": 1}
        assert (
         aluno_materia.salvar(al) ==
         mysql_mock.connection.cursor().lastrowid
        )
        mysql_mock.connection.cursor().execute.assert_called_once()
        mysql_mock.connection.commit.assert_called_once()
        mysql_mock.connection.cursor().close.assert_called_once()

    def test_buscar_todos(self, aluno_materia, mysql_mock):
        assert (
            aluno_materia.buscar_todos() ==
            [dict(record) for record in
             (mysql_mock.connection.cursor().fetchall)()]
        )
        (mysql_mock.connection.cursor()
         .execute.assert_called_once_with)("SELECT * FROM aluno_materia")
        mysql_mock.connection.cursor().close.assert_called_once()

    def test_buscar_por_id(self, aluno_materia, mysql_mock):
        aluno_materia_dict = {"id": 1, "idAluno": 1, "idMateria": 1}
        (mysql_mock.connection.cursor()
         .fetchone.return_value) = aluno_materia_dict
        assert aluno_materia.buscar_por_id(1) == aluno_materia_dict
        q = "SELECT * FROM aluno_materia WHERE id = %s"
        (mysql_mock.connection.cursor()
         .execute.assert_called_once_with)(q, (1,))
        mysql_mock.connection.cursor().close.assert_called_once()

    def test_editar(self, aluno_materia, mysql_mock):
        mysql_mock.connection.cursor().rowcount = 1
        aluno_materia_dict = {'idAluno': 1, 'idMateria': 2, 'id': 1}
        assert aluno_materia.editar(aluno_materia_dict)
        mysql_mock.connection.cursor().execute.assert_called_once()
        mysql_mock.connection.cursor().close.assert_called_once()
        mysql_mock.connection.commit.assert_called_once()

    def test_apagar(self, aluno_materia, mysql_mock):
        mysql_mock.connection.cursor().rowcount = 1
        assert aluno_materia.apagar(1)
        mysql_mock.connection.cursor().execute.assert_called_once()
        mysql_mock.connection.cursor().close.assert_called_once()
        mysql_mock.connection.commit.assert_called_once()
