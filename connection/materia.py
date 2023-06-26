class Materia:
    def __init__(self, mysql):
        self.mysql = mysql

    def buscar_todas(self, idUsuario, perfil):
        cursor = self.mysql.connection.cursor()
        if perfil == 'admin':
            cursor.execute("""
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
            """)
        else:
            cursor.execute("""
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
            """, (idUsuario,))
        materias = cursor.fetchall()
        cursor.close()

        return materias

    def buscar_materias_por_usuario(self, user_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("""SELECT DISTINCT m.id, m.nome
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
                        WHERE a.idusuario = %s""", (user_id, user_id))
        result = cursor.fetchall()
        cursor.close()

        return result

    def buscar_por_id(self, materia_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM materia WHERE id = %s", (materia_id,))
        materia = cursor.fetchone()
        cursor.close()
        return materia

    def adicionar_materia(self, nome, idresponsavel, idturma):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO materia (nome, idresponsavel, idturma) VALUES"
            " (%s, %s, %s)",
            (nome, idresponsavel, idturma))
        self.mysql.connection.commit()
        cursor.close()

    def editar_materia(self, materia_id, nome, idresponsavel, idturma):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "UPDATE materia SET nome = %s, idresponsavel = %s, idturma = %s"
            " WHERE id = %s",
            (nome, idresponsavel, idturma, materia_id))
        self.mysql.connection.commit()
        cursor.close()

    def deletar_materia(self, materia_id):
        cursor = self.mysql.connection.cursor()

        # Deletar registros associados em aluno_avaliacao_360
        cursor.execute(
            "DELETE aluno_avaliacao_360 FROM aluno_avaliacao_360 JOIN"
            " avaliacao_360 ON aluno_avaliacao_360.idavaliacao_360 ="
            " avaliacao_360.idavaliacao_360 WHERE"
            " avaliacao_360.idmateria = %s",
            (materia_id,))

        # Deletar registros associados em avaliacao_360
        cursor.execute("DELETE FROM avaliacao_360 WHERE idmateria = %s",
                       (materia_id,))

        # Deletar registros associados em grupo_aluno
        cursor.execute(
            "DELETE grupo_aluno FROM grupo_aluno JOIN grupo ON"
            " grupo_aluno.idgrupo = grupo.idgrupo WHERE grupo.idmateria = %s",
            (materia_id,))

        # Deletar registros associados em grupo
        cursor.execute("DELETE FROM grupo WHERE idmateria = %s", (materia_id,))

        # Deletar registros associados em aluno_notas_gerais
        cursor.execute(
            "DELETE aluno_notas_gerais FROM aluno_notas_gerais JOIN"
            " notas_gerais ON aluno_notas_gerais.idnotas_gerais ="
            " notas_gerais.idnotas_gerais WHERE notas_gerais.idmateria = %s",
            (materia_id,))

        # Deletar registros associados em notas_gerais
        cursor.execute("DELETE FROM notas_gerais WHERE idmateria = %s",
                       (materia_id,))

        # Deletar registros associados em avaliacao
        cursor.execute("DELETE FROM avaliacao WHERE idmateria = %s",
                       (materia_id,))

        # Finalmente, deletar a materia
        cursor.execute("DELETE FROM materia WHERE id = %s", (materia_id,))

        self.mysql.connection.commit()
        cursor.close()
