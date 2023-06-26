class Turma:
    def __init__(self, mySql):
        self.mysql = mySql

    def buscar_todos(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM turma")
        turmas = cursor.fetchall()
        cursor.close()
        return turmas

    def vincular_aluno(self, turma_id, aluno_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("INSERT INTO turma_aluno (idturma, idaluno)" +
                       "VALUES (%s, %s)", (turma_id, aluno_id))
        self.mysql.connection.commit()
        cursor.close()

    def remover_aluno(self, turma_id, aluno_id):
        cursor = self.mysql.connection.cursor()
        query = "DELETE FROM turma_aluno WHERE idturma=%s AND idaluno=%s"
        cursor.execute(query, (turma_id, aluno_id))
        self.mysql.connection.commit()
        cursor.close()

    def listar_alunos_nao_vinculados(self, turma_id):
        cursor = self.mysql.connection.cursor()
        query = (
            "SELECT * FROM aluno WHERE idaluno NOT IN "
            "(SELECT idaluno FROM turma_aluno WHERE idturma=%s)"
        )
        cursor.execute(query, (turma_id,))
        alunos = cursor.fetchall()
        cursor.close()
        return alunos

    def listar_alunos_vinculados(self, turma_id):
        query = (
            "SELECT * FROM aluno "
            "WHERE idaluno IN "
            "(SELECT idaluno FROM turma_aluno "
            "WHERE idturma=%s)"
        )
        cursor = self.mysql.connection.cursor()
        cursor.execute(query, (turma_id,))
        alunos = cursor.fetchall()
        cursor.close()
        return alunos

    def buscar_por_id(self, idturma):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM turma WHERE idturma = %s", (idturma,))
        turma = cursor.fetchone()
        cursor.close()
        return turma

    def adicionar_turma(self, nome, periodo):
        cursor = self.mysql.connection.cursor()
        cursor.execute("INSERT INTO turma (nome, periodo) VALUES (%s, %s)",
                       (nome, periodo))
        self.mysql.connection.commit()
        cursor.close()

    def editar_turma(self, turma_id, nome, periodo):
        cursor = self.mysql.connection.cursor()
        cursor.execute("UPDATE turma SET nome=%s, periodo=%s WHERE idturma=%s",
                       (nome, periodo, turma_id))
        self.mysql.connection.commit()
        cursor.close()

    def deletar_turma(self, turma_id):
        cursor = self.mysql.connection.cursor()

        cursor.execute(
            "DELETE aluno_notas_gerais FROM aluno_notas_gerais JOIN"
            " notas_gerais ON aluno_notas_gerais.idnotas_gerais ="
            " notas_gerais.idnotas_gerais JOIN materia ON"
            " notas_gerais.idmateria = materia.id WHERE materia.idturma = %s",
            (turma_id,))

        cursor.execute(
            "DELETE notas_gerais FROM notas_gerais JOIN materia ON"
            " notas_gerais.idmateria = materia.id WHERE materia.idturma = %s",
            (turma_id,))

        cursor.execute(
            "DELETE grupo_aluno FROM grupo_aluno JOIN grupo ON"
            " grupo_aluno.idgrupo = grupo.idgrupo JOIN materia ON"
            " grupo.idmateria = materia.id WHERE materia.idturma = %s",
            (turma_id,))

        cursor.execute(
            "DELETE grupo FROM grupo JOIN materia ON grupo.idmateria"
            " = materia.id WHERE materia.idturma = %s",
            (turma_id,))

        cursor.execute(
            "DELETE aluno_avaliacao_360 FROM aluno_avaliacao_360 JOIN"
            " avaliacao_360 ON aluno_avaliacao_360.idavaliacao_360"
            " = avaliacao_360.idavaliacao_360 JOIN materia ON"
            " avaliacao_360.idmateria = materia.id WHERE materia.idturma = %s",
            (turma_id,))

        cursor.execute(
            "DELETE avaliacao_360 FROM avaliacao_360 JOIN materia ON"
            " avaliacao_360.idmateria = materia.id WHERE materia.idturma = %s",
            (turma_id,))

        cursor.execute("DELETE FROM turma_aluno WHERE idturma = %s",
                       (turma_id,))

        cursor.execute("DELETE FROM materia WHERE idturma = %s", (turma_id,))

        cursor.execute("DELETE FROM turma WHERE idturma = %s", (turma_id,))

        self.mysql.connection.commit()
        cursor.close()
