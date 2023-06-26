from typing import List


class NotasGerais:
    def __init__(self, mySql):
        self.mysql = mySql

    def listar_notas_gerais(self) -> List[dict]:
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM notas_gerais")
        result = cur.fetchall()
        cur.close()
        return result

    def obter_notas_gerais_por_id(self, idnotas_gerais: int) -> dict:
        cur = self.mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM notas_gerais WHERE idnotas_gerais = %s",
            (idnotas_gerais,))
        result = cur.fetchone()
        cur.close()
        return result

    def buscar_por_id(self, id_notas_gerais):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
                        "SELECT * FROM notas_gerais WHERE idnotas_gerais = %s",
                        (id_notas_gerais,)
                      )

        notas_gerais = cursor.fetchone()
        cursor.close()
        return notas_gerais

    def inserir_notas_gerais(self, notas_gerais: dict) -> int:
        cur = self.mysql.connection.cursor()
        cur.execute(
            "INSERT INTO notas_gerais (avalicao_objetiva,"
            " avaliacao_dissertativa, uas, entregas, idmateria)"
            " VALUES (%s, %s, %s, %s, %s)",
            (notas_gerais['avalicao_objetiva'],
             notas_gerais['avaliacao_dissertativa'], notas_gerais['uas'],
             notas_gerais['entregas'], notas_gerais['idmateria']))
        self.mysql.connection.commit()
        result = cur.lastrowid
        cur.close()
        return result

    def atualizar_notas_gerais(self, idnotas_gerais: int, notas_gerais: dict):
        cur = self.mysql.connection.cursor()

        query_aluno = '''SELECT idAluno
                     FROM aluno_notas_gerais
                     WHERE idnotas_gerais = %s'''
        cur.execute(query_aluno, (idnotas_gerais,))
        aluno_id = cur.fetchone()[0]

        cur.execute(
            "UPDATE notas_gerais SET avalicao_objetiva = %s, "
            "avaliacao_dissertativa = %s, uas = %s, entregas = %s"
            " WHERE idnotas_gerais = %s",
            (notas_gerais['avalicao_objetiva'],
             notas_gerais['avaliacao_dissertativa'], notas_gerais['uas'],
             notas_gerais['entregas'], idnotas_gerais))
        self.mysql.connection.commit()
        cur.close()

        return aluno_id

    def idAluno_por_gerais(self, idnotas_gerais):
        cur = self.mysql.connection.cursor()

        query_aluno = '''SELECT idAluno
                     FROM aluno_notas_gerais
                     WHERE idnotas_gerais = %s'''
        cur.execute(query_aluno, (idnotas_gerais,))
        aluno_id = cur.fetchone()[0]
        cur.close()

        return aluno_id

    def excluir_gerais(self, id):
        cur = self.mysql.connection.cursor()

        cur.execute(
            "SELECT idAluno FROM aluno_notas_gerais WHERE idnotas_gerais = %s",
            (id,))
        aluno_id = cur.fetchone()[0]

        cur.execute("DELETE FROM aluno_notas_gerais WHERE idnotas_gerais = %s",
                    (id,))

        cur.execute("DELETE FROM notas_gerais WHERE idnotas_gerais = %s",
                    (id,))
        self.mysql.connection.commit()
        cur.close()

        return aluno_id

    def excluir_notas_gerais(self, idnotas_gerais: int) -> None:
        cur = self.mysql.connection.cursor()
        cur.execute(
            "DELETE FROM notas_gerais WHERE idnotas_gerais = %s",
            (idnotas_gerais,))
        self.mysql.connection.commit()
        cur.close()
