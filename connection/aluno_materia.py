from typing import Dict, List, Union


class AlunoMateria:

    def __init__(self, mysql):
        self.mysql = mysql

    def salvar(self, aluno_materia: Dict[str, Union[int]]) -> int:
        cursor = self.mysql.connection.cursor()
        sql = "INSERT INTO aluno_materia(idAluno, idMateria) VALUES(%s,%s)"
        values = (aluno_materia['idAluno'], aluno_materia['idMateria'])
        cursor.execute(sql, values)
        self.mysql.connection.commit()
        aluno_materia_id = cursor.lastrowid
        cursor.close()
        return aluno_materia_id

    def buscar_todos(self) -> List[Dict[str, Union[int]]]:
        cursor = self.mysql.connection.cursor()
        sql = "SELECT * FROM aluno_materia"
        cursor.execute(sql)
        aluno_materias = cursor.fetchall()
        cursor.close()
        return [dict(aluno_materia) for aluno_materia in aluno_materias]

    def buscar_por_id(
            self, aluno_materia_id: int) -> Union[Dict[str, Union[int]], None]:
        cursor = self.mysql.connection.cursor()
        sql = "SELECT * FROM aluno_materia WHERE id = %s"
        values = (aluno_materia_id,)
        cursor.execute(sql, values)
        aluno_materia = cursor.fetchone()
        cursor.close()
        if aluno_materia:
            return dict(aluno_materia)
        else:
            return None

    def editar(self, aluno_materia: Dict[str, Union[int]]) -> bool:
        cursor = self.mysql.connection.cursor()
        sql = "UPDATE aluno_materia SET idAluno=%s, idMateria=%s WHERE id=%s"
        values = (aluno_materia['idAluno'],
                  aluno_materia['idMateria'], aluno_materia['id'])
        cursor.execute(sql, values)
        self.mysql.connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0

    def apagar(self, aluno_materia_id: int) -> bool:
        cursor = self.mysql.connection.cursor()
        sql = "DELETE FROM aluno_materia WHERE id = %s"
        values = (aluno_materia_id,)
        cursor.execute(sql, values)
        self.mysql.connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0
