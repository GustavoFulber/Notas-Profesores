class TipoAvaliacao:
    def __init__(self, mySql):
        self.mysql = mySql

    def buscar_todos(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM tipo_avaliacao")
        tipo_avaliacoes = cur.fetchall()
        cur.close()
        return tipo_avaliacoes

    def buscar_por_id(self, idtipo_avaliacao):
        cur = self.mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM tipo_avaliacao WHERE idtipo_avaliacao = %s",
            (idtipo_avaliacao,))
        tipo_avaliacao = cur.fetchone()
        cur.close()
        return tipo_avaliacao

    def salvar(self, nome):
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO tipo_avaliacao (nome) VALUES (%s)", (nome,))
        self.mysql.connection.commit()
        cur.close()

    def editar(self, idtipo_avaliacao, nome):
        cur = self.mysql.connection.cursor()
        cur.execute(
            "UPDATE tipo_avaliacao SET nome = %s WHERE idtipo_avaliacao = %s",
            (nome, idtipo_avaliacao,))
        self.mysql.connection.commit()
        cur.close()

    def apagar(self, idtipo_avaliacao):
        cur = self.mysql.connection.cursor()
        cur.execute(
            "DELETE FROM tipo_avaliacao WHERE idtipo_avaliacao = %s",
            (idtipo_avaliacao,))
        self.mysql.connection.commit()
        cur.close()
