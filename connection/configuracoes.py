class Configuracoes:
    def __init__(self, mysql):
        self.mysql = mysql

    def buscar_todas(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT idconfiguracoes, chave, valor FROM configuracoes")
        result = cur.fetchall()
        cur.close()
        return result

    def buscar_por_id(self, id):
        cur = self.mysql.connection.cursor()
        cur.execute(
            "SELECT idconfiguracoes, chave, valor FROM configuracoes "
            "WHERE idconfiguracoes = %s",
            (id,))
        result = cur.fetchone()
        cur.close()
        return result

    def editar(self, id, configuracoes):
        cur = self.mysql.connection.cursor()
        cur.execute(
            "UPDATE configuracoes SET valor = %s WHERE idconfiguracoes = %s",
            (configuracoes['valor'], id))
        self.mysql.connection.commit()
        cur.close()

    def buscar_por_chave(self, chave):
        cur = self.mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM configuracoes WHERE chave = %s",
            (chave,)
        )
        result = cur.fetchone()
        cur.close()
        return result

    def editar_por_chave(self, chave, valor):
        cur = self.mysql.connection.cursor()
        cur.execute(
            "UPDATE configuracoes SET valor = %s WHERE chave = %s",
            (valor, chave)
        )
        self.mysql.connection.commit()
        cur.close()

    def apagar(self, id):
        cur = self.mysql.connection.cursor()
        cur.execute(
            "DELETE FROM configuracoes WHERE idconfiguracoes = %s", (id,))
        self.mysql.connection.commit()
        cur.close()

    def salvar(self, configuracoes):
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO configuracoes (chave, valor) VALUES (%s, %s)",
                    (configuracoes['chave'], configuracoes['valor']))
        self.mysql.connection.commit()
        id = cur.lastrowid
        cur.close()
        return id
