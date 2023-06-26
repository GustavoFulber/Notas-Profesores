import unittest
from unittest.mock import MagicMock

from flask_mysqldb import MySQL

from connection.aluno import Aluno


class TestAluno(unittest.TestCase):
    def setUp(self):
        # Configurar o ambiente de teste
        self.mysql = MagicMock(spec=MySQL)
        self.aluno = Aluno(self.mysql)

    def test_buscar_por_id(self):
        # Simular o comportamento do banco de dados
        cursor = self.mysql.connection.cursor()
        cursor.fetchone.return_value = ('João', 8.5)
        self.mysql.connection.cursor.return_value = cursor

        # Executar o método a ser testado
        aluno = self.aluno.buscar_por_id(1)

        # Verificar o resultado
        self.assertEqual(aluno, ('João', 8.5))
        cursor.execute.assert_called_once_with(
            "SELECT * FROM aluno WHERE idAluno=%s", (1,)
        )
        cursor.close.assert_called_once()

    def test_usuarios_sem_alunos(self):
        # Simular o comportamento do banco de dados
        cursor = self.mysql.connection.cursor()
        cursor.fetchall.return_value = [('João',), ('Maria',)]
        self.mysql.connection.cursor.return_value = cursor

        # Executar o método a ser testado
        usuarios = self.aluno.usuarios_sem_alunos()

        # Verificar o resultado
        self.assertEqual(usuarios, [('João',), ('Maria',)])
        cursor.execute.assert_called_once_with(
            "SELECT u.* FROM usuario AS u LEFT JOIN "
            "aluno AS a ON u.idusuario = a.idusuario "
            "WHERE a.idusuario IS NULL AND "
            " u.verificado = 1 AND u.aprovado = 1;"
        )
        cursor.close.assert_called_once()

    def test_get_notas_gerais(self):
        # Simular o comportamento do banco de dados
        cursor = self.mysql.connection.cursor()
        cursor.fetchall.return_value = [(8.5,)]
        self.mysql.connection.cursor.return_value = cursor

        # Executar o método a ser testado
        notas = self.aluno.get_notas_gerais()

        # Verificar o resultado
        self.assertEqual(notas, [(8.5,)])
        cursor.execute.assert_called_once_with("SELECT * FROM notas_gerais")
        cursor.close.assert_called_once()

    def test_get_avaliacao_360(self):
        # Simular o comportamento do banco de dados
        cursor = self.mysql.connection.cursor()
        cursor.fetchall.return_value = [(7.5,)]
        self.mysql.connection.cursor.return_value = cursor

        # Executar o método a ser testado
        avaliacoes = self.aluno.get_avaliacao_360()

        # Verificar o resultado
        self.assertEqual(avaliacoes, [(7.5,)])
        cursor.execute.assert_called_once_with("SELECT * FROM avaliacao_360")
        cursor.close.assert_called_once()

    def test_buscar_id_por_usuario(self):
        # Simular o comportamento do banco de dados
        cursor = self.mysql.connection.cursor()
        cursor.fetchone.return_value = (1,)
        self.mysql.connection.cursor.return_value = cursor

        # Executar o método a ser testado
        id_aluno = self.aluno.buscar_id_por_usuario(1)

        # Verificar o resultado
        self.assertEqual(id_aluno, 1)
        cursor.execute.assert_called_once_with(
            "SELECT idaluno FROM aluno WHERE idusuario = %s", (1,)
        )
        cursor.close.assert_called_once()

    def test_buscar_avaliacoes_por_usuario_au(self):
        # Simular o comportamento do banco de dados
        cursor = self.mysql.connection.cursor()
        cursor.fetchall.return_value = [
            (1, True, 1, 2, 1, 'João', 1, 'Matemática'),
            (2, False, 3, 4, 1, 'Maria', 1, 'História')
        ]
        self.mysql.connection.cursor.return_value = cursor

        # Executar o método a ser testado
        avaliacoes = self.aluno.buscar_avaliacoes_por_usuario_au(1)

        # Verificar o resultado
        self.assertEqual(
            avaliacoes,
            [
                {
                    'idavaliacao': 1,
                    'completo': True,
                    'idmateria': 1,
                    'idaluno_avaliado': 2,
                    'idaluno_realizando': 1,
                    'nome_aluno_avaliado': 'João',
                    'idusuario': 1,
                    'nome_materia': 'Matemática'
                },
                {
                    'idavaliacao': 2,
                    'completo': False,
                    'idmateria': 3,
                    'idaluno_avaliado': 4,
                    'idaluno_realizando': 1,
                    'nome_aluno_avaliado': 'Maria',
                    'idusuario': 1,
                    'nome_materia': 'História'
                }
            ]
        )
        cursor.execute.assert_called_once_with(
            "SELECT avaliacao.*, aluno_avaliado.nome AS nome_aluno_avaliado, "
            "aluno_realizando.idusuario, materia.nome AS nome_materia "
            "FROM avaliacao "
            "INNER JOIN aluno AS aluno_avaliado ON avaliacao.idaluno_avaliado"
            " = aluno_avaliado.idaluno "
            "INNER JOIN aluno AS aluno_realizando "
            "ON avaliacao.idaluno_realizando"
            " = aluno_realizando.idaluno "
            "INNER JOIN materia ON avaliacao.idmateria = materia.id "
            "WHERE aluno_realizando.idusuario = %s "
            "and avaliacao.completo = false",
            (1,)
        )
        cursor.close.assert_called_once()

    def test_buscar_alunos_por_grupo(self):
        # Simular o comportamento do banco de dados
        cursor = self.mysql.connection.cursor()
        cursor.fetchall.return_value = [('João', 1), ('Maria', 2)]
        self.mysql.connection.cursor.return_value = cursor

        # Executar o método a ser testado
        alunos = self.aluno.buscar_alunos_por_grupo(1)

        # Verificar o resultado
        self.assertEqual(alunos, [('João', 1), ('Maria', 2)])
        cursor.execute.assert_called_once_with(
            "SELECT * FROM aluno WHERE idaluno IN "
            "(SELECT idaluno FROM grupo_aluno WHERE idgrupo = %s)", (1,)
        )
        cursor.close.assert_called_once()

    def test_criar_avaliacao(self):
        # Simular o comportamento do banco de dados
        cursor = self.mysql.connection.cursor()

        # Executar o método a ser testado
        self.aluno.criar_avaliacao(True, 1, 2, 3)

        # Verificar o comportamento
        cursor.execute.assert_called_once_with(
            "INSERT INTO avaliacao (completo, idmateria, "
            "idaluno_avaliado, idaluno_realizando) "
            "VALUES (%s, %s, %s, %s)", (True, 1, 2, 3)
        )
        self.mysql.connection.commit.assert_called_once()
        cursor.close.assert_called_once()

    def test_criar_autoavaliacao(self):
        # Simular o comportamento do banco de dados
        cursor = self.mysql.connection.cursor()

        # Executar o método a ser testado
        self.aluno.criar_autoavaliacao(True, 1, 2)

        # Verificar o comportamento
        cursor.execute.assert_called_once_with(
            "INSERT INTO avaliacao (completo, idmateria, "
            "idaluno_avaliado, idaluno_realizando) "
            "VALUES (%s, %s, %s, %s)", (True, 1, 2, 2)
        )
        self.mysql.connection.commit.assert_called_once()
        cursor.close.assert_called_once()

    def test_buscar_avaliacoes_por_usuario(self):
        # Simular o comportamento do banco de dados
        cursor = self.mysql.connection.cursor()
        cursor.fetchall.return_value = [(1, 2, 3), (4, 5, 6)]
        self.mysql.connection.cursor.return_value = cursor

        # Executar o método a ser testado
        avaliacoes = self.aluno.buscar_avaliacoes_por_usuario(1)

        # Verificar o resultado
        self.assertEqual(avaliacoes, [(1, 2, 3), (4, 5, 6)])
        cursor.execute.assert_called_once_with(
            "SELECT a.* FROM avaliacao a JOIN aluno al "
            "ON a.idaluno_realizando = al.idaluno "
            "WHERE al.idusuario = %s", (1,)
        )
        cursor.close.assert_called_once()

    def test_salvar_relacao_turma_aluno(self):
        # Simular o comportamento do banco de dados
        cursor = self.mysql.connection.cursor()

        # Executar o método a ser testado
        self.aluno.salvar_relacao_turma_aluno(1, 2)

        # Verificar o comportamento
        cursor.execute.assert_called_once_with(
            "INSERT INTO turma_aluno (idturma, idaluno) VALUES (%s, %s)",
            (2, 1)
        )
        self.mysql.connection.commit.assert_called_once()
        cursor.close.assert_called_once()

    def test_get_notas_finais(self):
        # Simular o comportamento do banco de dados
        cursor = self.mysql.connection.cursor()
        cursor.fetchall.return_value = [(8.5,), (7.0,), (9.0,)]
        self.mysql.connection.cursor.return_value = cursor

        # Executar o método a ser testado
        notas_finais = self.aluno.get_notas_finais()

        # Verificar o resultado
        self.assertEqual(notas_finais, [(8.5,), (7.0,), (9.0,)])
        cursor.execute.assert_called_once_with("SELECT nota FROM aluno")
        cursor.close.assert_called_once()

    def test_buscar_todos(self):
        # Simular o comportamento do banco de dados
        cursor = self.mysql.connection.cursor()
        cursor.fetchall.return_value = [
                                        ('João', 1),
                                        ('Maria', 2),
                                        ('Carlos', 3)
                                        ]
        self.mysql.connection.cursor.return_value = cursor

        # Executar o método a ser testado
        alunos = self.aluno.buscar_todos()

        # Verificar o resultado
        self.assertEqual(alunos, [('João', 1), ('Maria', 2), ('Carlos', 3)])
        cursor.execute.assert_called_once_with("SELECT * FROM aluno")
        cursor.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
