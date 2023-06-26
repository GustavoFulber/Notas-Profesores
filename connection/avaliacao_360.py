class Avaliacao360:

    def __init__(self, mysql):
        self.mysql = mysql

    def salvar(self, avaliacao):
        cursor = self.mysql.connection.cursor()
        query = '''INSERT INTO avaliacao_360 (comunicacao, cognitivo,
            autogestao, autonomia, protagonismo, interacao, tipo_avaliacao,
            idmateria)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
        values = (avaliacao['comunicacao'], avaliacao['cognitivo'],
                  avaliacao['autogestao'], avaliacao['autonomia'],
                  avaliacao['protagonismo'], avaliacao['interacao'],
                  avaliacao['idtipo_avaliacao'], avaliacao['idmateria'])
        cursor.execute(query, values)
        self.mysql.connection.commit()
        idavaliacao = cursor.lastrowid
        cursor.close()
        return idavaliacao

    def buscar_por_id(self, idavaliacao_360):
        cursor = self.mysql.connection.cursor()
        query = "SELECT * FROM avaliacao_360 WHERE idavaliacao_360 = %s"
        values = (idavaliacao_360,)
        cursor.execute(query, values)
        avaliacao = cursor.fetchone()
        cursor.close()
        return avaliacao

    def buscar_todos(self):
        cursor = self.mysql.connection.cursor()
        query = "SELECT * FROM avaliacao_360"
        cursor.execute(query)
        avaliacoes = cursor.fetchall()
        cursor.close()
        return avaliacoes

    def editar(self, idavaliacao_360, avaliacao):
        cursor = self.mysql.connection.cursor()

        query_aluno = '''SELECT idAluno
                             FROM aluno_avaliacao_360
                             WHERE idavaliacao_360 = %s'''
        cursor.execute(query_aluno, (idavaliacao_360,))
        aluno_id = cursor.fetchone()[0]

        query = '''UPDATE avaliacao_360
                   SET comunicacao=%s, cognitivo=%s, autogestao=%s,
                    autonomia=%s, protagonismo=%s, interacao=%s,
                    tipo_avaliacao=%s
                    WHERE idavaliacao_360=%s'''
        values = (avaliacao['comunicacao'], avaliacao['cognitivo'],
                  avaliacao['autogestao'], avaliacao['autonomia'],
                  avaliacao['protagonismo'], avaliacao['interacao'],
                  avaliacao['idtipo_avaliacao'], idavaliacao_360)
        cursor.execute(query, values)
        self.mysql.connection.commit()
        cursor.close()

        return aluno_id

    def excluir_avaliacao360(self, id):
        cur = self.mysql.connection.cursor()

        cur.execute(
            "SELECT idAluno FROM aluno_avaliacao_360"
            " WHERE idavaliacao_360 = %s",
            (id,))
        aluno_id = cur.fetchone()[0]

        cur.execute(
            "DELETE FROM aluno_avaliacao_360 WHERE idavaliacao_360 = %s",
            (id,))

        cur.execute("DELETE FROM avaliacao_360 WHERE idavaliacao_360 = %s",
                    (id,))
        self.mysql.connection.commit()
        cur.close()

        return aluno_id

    def idAluno_por_360(self, idavaliacao_360):
        cursor = self.mysql.connection.cursor()

        query_aluno = '''SELECT idAluno
                                     FROM aluno_avaliacao_360
                                     WHERE idavaliacao_360 = %s'''
        cursor.execute(query_aluno, (idavaliacao_360,))
        aluno_id = cursor.fetchone()[0]
        cursor.close()

        return aluno_id

    def apagar(self, idavaliacao_360):
        cursor = self.mysql.connection.cursor()
        query = "DELETE FROM avaliacao_360 WHERE idavaliacao_360 = %s"
        values = (idavaliacao_360,)
        cursor.execute(query, values)
        self.mysql.connection.commit()
        cursor.close()
