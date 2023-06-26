from typing import Dict, List


class AlunoAvaliacao360:
    def __init__(self, mySql):
        self.mysql = mySql

    def salvar(self, aluno_avaliacao: Dict[str, int]) -> int:
        cursor = self.mysql.connection.cursor()
        sql = "INSERT INTO aluno_avaliacao_360(idAluno," \
              " idavaliacao_360) VALUES(%s,%s)"
        values = (aluno_avaliacao['idAluno'],
                  aluno_avaliacao['idavaliacao_360'])
        cursor.execute(sql, values)
        self.mysql.connection.commit()
        aluno_avaliacao_id = cursor.lastrowid
        cursor.close()
        return aluno_avaliacao_id

    def editar(self, aluno_avaliacao: Dict[str, int]) -> None:
        cursor = self.mysql.connection.cursor()
        sql = "UPDATE aluno_avaliacao_360 SET idAluno=%s," \
              " idavaliacao_360=%s WHERE id=%s"
        values = (aluno_avaliacao['idAluno'],
                  aluno_avaliacao['idavaliacao_360'], aluno_avaliacao['id'])
        cursor.execute(sql, values)
        self.mysql.connection.commit()
        cursor.close()

    def apagar(self, aluno_avaliacao_id: int) -> None:
        cursor = self.mysql.connection.cursor()
        sql = "DELETE FROM aluno_avaliacao_360 WHERE id=%s"
        cursor.execute(sql, (aluno_avaliacao_id,))
        self.mysql.connection.commit()
        cursor.close()

    def apagar_aluno_id(self, idAluno: int) -> None:
        cursor = self.mysql.connection.cursor()
        sql = "DELETE FROM aluno_avaliacao_360 WHERE idAluno = %s;" \
              " DELETE FROM avaliacao_360 WHERE idavaliacao_360 IN (SELECT" \
              " idavaliacao_360 FROM aluno_avaliacao_360 WHERE idAluno = %s);"
        cursor.execute(sql, (idAluno, idAluno))
        self.mysql.connection.commit()
        cursor.close()

    def buscar_por_id(self, aluno_avaliacao_id: int) -> Dict[str, int]:
        cursor = self.mysql.connection.cursor()
        sql = "SELECT * FROM aluno_avaliacao_360 WHERE id=%s"
        cursor.execute(sql, (aluno_avaliacao_id,))
        aluno_avaliacao = cursor.fetchone()
        cursor.close()
        if aluno_avaliacao:
            return {'id': aluno_avaliacao[0], 'idAluno': aluno_avaliacao[1],
                    'idavaliacao_360': aluno_avaliacao[2]}
        return None

    def buscar_por_idAluno(self, idAluno):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            'SELECT tipo_avaliacao.nome, avaliacao_360.comunicacao,'
            ' avaliacao_360.cognitivo, avaliacao_360.autogestao,'
            ' avaliacao_360.autonomia, avaliacao_360.protagonismo,'
            ' avaliacao_360.interacao FROM aluno_avaliacao_360 JOIN'
            ' avaliacao_360 ON aluno_avaliacao_360.idavaliacao_360 ='
            ' avaliacao_360.idavaliacao_360 JOIN tipo_avaliacao ON'
            ' avaliacao_360.tipo_avaliacao = tipo_avaliacao.idtipo_avaliacao'
            ' WHERE aluno_avaliacao_360.idAluno = %s',
            [idAluno])
        avaliacoes360 = cursor.fetchall()
        cursor.close()
        return avaliacoes360

    def buscar_por_idAluno_materia(self, idAluno, idmateria):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            'SELECT tipo_avaliacao.nome, avaliacao_360.comunicacao,'
            ' avaliacao_360.cognitivo, avaliacao_360.autogestao,'
            ' avaliacao_360.autonomia, avaliacao_360.protagonismo,'
            ' avaliacao_360.interacao FROM aluno_avaliacao_360 JOIN'
            ' avaliacao_360 ON aluno_avaliacao_360.idavaliacao_360 ='
            ' avaliacao_360.idavaliacao_360 JOIN tipo_avaliacao ON'
            ' avaliacao_360.tipo_avaliacao = tipo_avaliacao.idtipo_avaliacao'
            ' and avaliacao_360.idmateria = %s'
            ' WHERE aluno_avaliacao_360.idAluno = %s',
            [idmateria, idAluno])
        avaliacoes360 = cursor.fetchall()
        cursor.close()
        return avaliacoes360

    def atualizar_completo(self, idavaliacao, completo=True):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "UPDATE avaliacao SET completo = %s WHERE idavaliacao = %s",
            (completo, idavaliacao))
        self.mysql.connection.commit()
        cursor.close()

    def buscar_por_id_ul(self, idavaliacao):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM avaliacao WHERE idavaliacao = %s"
            " and completo = false",
            (idavaliacao,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def buscar_por_idAluno_comid(self, idAluno, idmateria):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            'SELECT avaliacao_360.idavaliacao_360, tipo_avaliacao.nome,'
            ' avaliacao_360.comunicacao, avaliacao_360.cognitivo,'
            ' avaliacao_360.autogestao, avaliacao_360.autonomia,'
            ' avaliacao_360.protagonismo, avaliacao_360.interacao'
            ' FROM aluno_avaliacao_360 JOIN avaliacao_360 ON'
            ' aluno_avaliacao_360.idavaliacao_360 ='
            ' avaliacao_360.idavaliacao_360 JOIN tipo_avaliacao ON'
            ' avaliacao_360.tipo_avaliacao = tipo_avaliacao.idtipo_avaliacao'
            ' and avaliacao_360.idmateria = %s'
            ' WHERE aluno_avaliacao_360.idAluno = %s',
            [idmateria, idAluno])
        avaliacoes360 = cursor.fetchall()
        cursor.close()
        return avaliacoes360

    def buscar_todos(self) -> List[Dict[str, int]]:
        cursor = self.mysql.connection.cursor()
        sql = "SELECT * FROM aluno_avaliacao_360"
        cursor.execute(sql)
        aluno_avaliacao_list = cursor.fetchall()
        cursor.close()
        return [{'id': aluno_avaliacao[0], 'idAluno': aluno_avaliacao[1],
                 'idavaliacao_360': aluno_avaliacao[2]} for aluno_avaliacao in
                aluno_avaliacao_list]

    def verificarNotaVazia(self, notas):
        if (notas.form['pComunicacao'].strip() == ''):
            return False

        if (notas.form['pCognitivo'].strip() == ''):
            return False

        if (notas.form['pAutogestao'].strip() == ''):
            return False

        if (notas.form['pAutonomia'].strip() == ''):
            return False

        if (notas.form['pProtagonismo'].strip() == ''):
            return False

        if (notas.form['pInteracao'].strip() == ''):
            return False

        return True

    def verificarNotaMaiorQueDez(self, notas):
        if (float(notas.form['pComunicacao']) > 10.0):
            return False

        if (float(notas.form['pCognitivo']) > 10.0):
            return False

        if (float(notas.form['pAutogestao']) > 10.0):
            return False

        if (float(notas.form['pAutonomia']) > 10.0):
            return False

        if (float(notas.form['pProtagonismo']) > 10.0):
            return False

        if (float(notas.form['pInteracao']) > 10.0):
            return False

        return True
