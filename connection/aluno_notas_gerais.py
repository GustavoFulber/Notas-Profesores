from typing import Dict, List


class AlunoNotasGerais:
    def __init__(self, mysql):
        self.mysql = mysql

    def buscar_todos(self) -> List[Dict]:
        cursor = self.mysql.connection.cursor()
        cursor.execute('SELECT * FROM aluno_notas_gerais')
        alunos_notas_gerais = cursor.fetchall()
        cursor.close()
        return alunos_notas_gerais

    def buscar_por_id(self, id_aluno_notas_gerais: int) -> Dict:
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM aluno_notas_gerais WHERE id=%s',
            (id_aluno_notas_gerais,))
        aluno_notas_gerais = cursor.fetchone()
        cursor.close()
        return aluno_notas_gerais

    def buscar_por_idAluno(self, idAluno):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            'SELECT notas_gerais.avalicao_objetiva,'
            ' notas_gerais.avaliacao_dissertativa, notas_gerais.uas,'
            ' notas_gerais.entregas FROM aluno_notas_gerais JOIN notas_gerais'
            ' ON aluno_notas_gerais.idnotas_gerais ='
            ' notas_gerais.idnotas_gerais WHERE'
            ' aluno_notas_gerais.idAluno = %s',
            [idAluno])
        notasGerais = cursor.fetchall()
        cursor.close()
        return notasGerais

    def buscar_por_idAluno_materia(self, idAluno, idmateria):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            'SELECT notas_gerais.avalicao_objetiva,'
            ' notas_gerais.avaliacao_dissertativa, notas_gerais.uas,'
            ' notas_gerais.entregas FROM aluno_notas_gerais JOIN notas_gerais'
            ' ON aluno_notas_gerais.idnotas_gerais ='
            ' notas_gerais.idnotas_gerais and notas_gerais.idmateria = %s'
            ' WHERE aluno_notas_gerais.idAluno = %s',
            [idmateria, idAluno])
        notasGerais = cursor.fetchall()
        cursor.close()
        return notasGerais

    def buscar_por_idAluno_comid(self, idAluno, idmateria):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            'SELECT notas_gerais.idnotas_gerais,'
            ' notas_gerais.avalicao_objetiva,'
            ' notas_gerais.avaliacao_dissertativa, notas_gerais.uas,'
            ' notas_gerais.entregas FROM aluno_notas_gerais JOIN notas_gerais'
            ' ON aluno_notas_gerais.idnotas_gerais ='
            ' notas_gerais.idnotas_gerais and notas_gerais.idmateria = %s'
            ' WHERE aluno_notas_gerais.idAluno = %s',
            [idmateria, idAluno])
        notasGerais = cursor.fetchall()
        cursor.close()
        return notasGerais

    def criar(self, aluno_notas_gerais: Dict[str, int]) -> int:
        cursor = self.mysql.connection.cursor()
        sql = "INSERT INTO aluno_notas_gerais(idAluno, idnotas_gerais)" \
              " VALUES(%s, %s)"
        values = (aluno_notas_gerais['idAluno'],
                  aluno_notas_gerais['idnotas_gerais'])
        cursor.execute(sql, values)
        self.mysql.connection.commit()
        id_aluno_notas_gerais = cursor.lastrowid
        cursor.close()
        return id_aluno_notas_gerais

    def editar(self, id_aluno_notas_gerais: int,
               aluno_notas_gerais: Dict[str, int]) -> None:
        cursor = self.mysql.connection.cursor()
        sql = "UPDATE aluno_notas_gerais SET idAluno=%s," \
              " idnotas_gerais=%s WHERE id=%s"
        values = (aluno_notas_gerais['idAluno'],
                  aluno_notas_gerais['idnotas_gerais'], id_aluno_notas_gerais)
        cursor.execute(sql, values)
        self.mysql.connection.commit()
        cursor.close()

    def apagar(self, id_aluno_notas_gerais: int) -> None:
        cursor = self.mysql.connection.cursor()
        cursor.execute('DELETE FROM aluno_notas_gerais WHERE id=%s',
                       (id_aluno_notas_gerais,))
        self.mysql.connection.commit()
        cursor.close()

    def apagar_aluno_id(self, idAluno: int) -> None:
        cursor = self.mysql.connection.cursor()
        sql = "DELETE FROM aluno_notas_gerais WHERE idAluno = %s; DELETE" \
              " FROM notas_gerais WHERE idnotas_gerais IN (SELECT" \
              " idnotas_gerais FROM aluno_notas_gerais WHERE idAluno = %s);"
        cursor.execute(sql, (idAluno, idAluno))
        self.mysql.connection.commit()
        cursor.close()

    def verificarNotaVazia(self, notas):
        if (notas.form['avaliacao_objetiva'].strip() == ''):
            return False

        if (notas.form['avaliacao_dissertativa'].strip() == ''):
            return False

        if (notas.form['uas'].strip() == ''):
            return False

        if (notas.form['entregas'].strip() == ''):
            return False

        return True

    def verificarNotaMaiorQueDez(self, notas):
        if (float(notas.form['avaliacao_objetiva']) > 10.0):
            return False

        if (float(notas.form['avaliacao_dissertativa']) > 10.0):
            return False

        if (float(notas.form['uas']) > 10.0):
            return False

        if (float(notas.form['entregas']) > 10.0):
            return False

        return True
