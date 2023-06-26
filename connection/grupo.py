class Grupo:
    def __init__(self, mysql):
        self.mysql = mysql

    def buscar_por_materia(self, materia_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM grupo WHERE idmateria = %s",
                       (materia_id,))
        grupos = cursor.fetchall()
        cursor.close()
        return grupos

    def buscar_por_id(self, grupo_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM grupo WHERE idgrupo = %s", (grupo_id,))
        grupo = cursor.fetchone()
        cursor.close()
        return grupo

    def adicionar_grupo(self, nome, materia_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("INSERT INTO grupo (nome, idmateria) VALUES (%s, %s)",
                       (nome, materia_id))
        self.mysql.connection.commit()
        cursor.close()

    def editar_grupo(self, grupo_id, nome):
        cursor = self.mysql.connection.cursor()
        cursor.execute("UPDATE grupo SET nome = %s WHERE idgrupo = %s",
                       (nome, grupo_id))
        self.mysql.connection.commit()
        cursor.close()

    def deletar_grupo(self, grupo_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("DELETE FROM grupo WHERE idgrupo = %s", (grupo_id,))
        self.mysql.connection.commit()
        cursor.close()

    def vincular_aluno(self, grupo_id, aluno_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO grupo_aluno (idgrupo, idaluno) VALUES (%s, %s)",
            (grupo_id, aluno_id))
        self.mysql.connection.commit()
        cursor.close()

    def remover_aluno(self, grupo_id, aluno_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "DELETE FROM grupo_aluno WHERE idgrupo=%s AND idaluno=%s",
            (grupo_id, aluno_id))
        self.mysql.connection.commit()
        cursor.close()

    def listar_alunos_nao_vinculados(self, grupo_id, idmateria):
        cursor = self.mysql.connection.cursor()

        query = """
            SELECT aluno.*
            FROM aluno
            JOIN turma_aluno ON aluno.idaluno = turma_aluno.idaluno
            JOIN materia ON turma_aluno.idturma = materia.idturma
            WHERE materia.id = %s
            AND aluno.idaluno NOT IN (
                SELECT idaluno FROM grupo_aluno WHERE idgrupo = %s
            )
        """

        cursor.execute(query, (idmateria, grupo_id))
        alunos = cursor.fetchall()

        cursor.close()

        return alunos

    def listar_alunos_vinculados(self, grupo_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM aluno WHERE idaluno IN (SELECT idaluno FROM"
            " grupo_aluno WHERE idgrupo=%s)",
            (grupo_id,))
        alunos = cursor.fetchall()
        cursor.close()
        return alunos
