from typing import Dict


class Aluno:
    def __init__(self, mySql):
        self.mysql = mySql

    def buscar_por_id(self, id_aluno):
        cursor = self.mysql.connection.cursor()
        sql = "SELECT * FROM aluno WHERE idAluno=%s"
        cursor.execute(sql, (id_aluno,))
        aluno = cursor.fetchone()
        cursor.close()
        return aluno

    def usuarios_sem_alunos(self):
        cursor = self.mysql.connection.cursor()
        sql = "SELECT u.* FROM usuario AS u LEFT JOIN aluno AS a ON" \
              " u.idusuario = a.idusuario WHERE a.idusuario IS NULL " \
              "AND u.verificado = 1 AND u.aprovado = 1;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_notas_gerais(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM notas_gerais")
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_avaliacao_360(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM avaliacao_360")
        result = cursor.fetchall()
        cursor.close()
        return result

    def buscar_id_por_usuario(self, user_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT idaluno FROM aluno WHERE idusuario = %s",
                       (user_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]
        else:
            return None

    def buscar_avaliacoes_por_usuario_au(self, idusuario):
        cursor = self.mysql.connection.cursor()
        cursor.execute("""
            SELECT avaliacao.*, aluno_avaliado.nome AS nome_aluno_avaliado,
            aluno_realizando.idusuario, materia.nome AS nome_materia
            FROM avaliacao
            INNER JOIN aluno AS aluno_avaliado ON avaliacao.idaluno_avaliado
            = aluno_avaliado.idaluno
            INNER JOIN aluno AS aluno_realizando
            ON avaliacao.idaluno_realizando = aluno_realizando.idaluno
            INNER JOIN materia ON avaliacao.idmateria = materia.id
            WHERE aluno_realizando.idusuario = %s and
            avaliacao.completo = false
        """, (idusuario,))
        result = cursor.fetchall()
        avaliacoes = []
        for row in result:
            avaliacao = {
                'idavaliacao': row[0],
                'completo': row[1],
                'idmateria': row[2],
                'idaluno_avaliado': row[3],
                'idaluno_realizando': row[4],
                'nome_aluno_avaliado': row[5],
                'idusuario': row[6],
                'nome_materia': row[7]
            }
            avaliacoes.append(avaliacao)
        cursor.close()
        return avaliacoes

    def buscar_alunos_por_grupo(self, idgrupo):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM aluno WHERE idaluno IN (SELECT idaluno FROM"
            " grupo_aluno WHERE idgrupo = %s)",
            (idgrupo,))
        alunos = cursor.fetchall()
        cursor.close()
        return alunos

    def criar_avaliacao(self, completo, idmateria, idaluno_avaliado,
                        idaluno_realizando):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO avaliacao (completo, idmateria, idaluno_avaliado,"
            " idaluno_realizando) VALUES (%s, %s, %s, %s)",
            (completo, idmateria, idaluno_avaliado, idaluno_realizando))
        self.mysql.connection.commit()
        cursor.close()

    def criar_autoavaliacao(self, completo, idmateria, idaluno):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO avaliacao (completo, idmateria, idaluno_avaliado,"
            " idaluno_realizando) VALUES (%s, %s, %s, %s)",
            (completo, idmateria, idaluno, idaluno))
        self.mysql.connection.commit()
        cursor.close()

    def buscar_avaliacoes_por_usuario(self, idusuario):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "SELECT a.* FROM avaliacao a JOIN aluno al ON a.idaluno_realizando"
            " = al.idaluno WHERE al.idusuario = %s",
            (idusuario,))
        avaliacoes = cursor.fetchall()
        cursor.close()
        return avaliacoes

    def salvar_relacao_turma_aluno(self, id_aluno, id_turma):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO turma_aluno (idturma, idaluno) VALUES (%s, %s)",
            (id_turma, id_aluno))
        self.mysql.connection.commit()
        cursor.close()

    def get_notas_finais(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT nota FROM aluno")
        result = cursor.fetchall()
        cursor.close()
        return result

    def buscar_todos(self):
        cursor = self.mysql.connection.cursor()
        sql = "SELECT * FROM aluno"
        cursor.execute(sql)
        alunos = cursor.fetchall()
        cursor.close()
        return alunos

    def buscar_aluno_por_nome(self, nome):
        cursor = self.mysql.connection.cursor()
        sql = "SELECT * FROM aluno WHERE nome = %s"
        cursor.execute(sql, (nome,))
        aluno = cursor.fetchone()
        cursor.close()
        return aluno

    def buscar_todos_com_usuarios(self):
        cursor = self.mysql.connection.cursor()
        sql = """
        SELECT aluno.idAluno, aluno.nome, usuario.nome
        FROM aluno
        LEFT JOIN usuario ON aluno.idusuario = usuario.idusuario
        """
        cursor.execute(sql)
        alunos = cursor.fetchall()
        cursor.close()

        alunos_com_usuarios = []
        for aluno in alunos:
            alunos_com_usuarios.append({
                'idAluno': aluno[0],
                'nome': aluno[1],
                'usuario': aluno[2] if aluno[2] else 'Sem Usuário',
            })

        return alunos_com_usuarios

    def vincular_usuario(self, idAluno, idusuario):
        cursor = self.mysql.connection.cursor()
        sql = "UPDATE aluno SET idusuario = %s WHERE idAluno = %s"
        cursor.execute(sql, (idusuario, idAluno))
        self.mysql.connection.commit()
        cursor.close()

    def desvincular_usuario(self, idAluno):
        cursor = self.mysql.connection.cursor()
        sql = "UPDATE aluno SET idusuario = NULL WHERE idAluno = %s"
        cursor.execute(sql, (idAluno,))
        self.mysql.connection.commit()
        cursor.close()

    def salvar(self, aluno: Dict[str, str]) -> int:
        cursor = self.mysql.connection.cursor()
        sql = "INSERT INTO aluno(nome, nota)" \
              "VALUES(%s,%s)"
        values = (aluno['nome'], aluno['nota'])
        cursor.execute(sql, values)
        self.mysql.connection.commit()
        aluno_id = cursor.lastrowid
        cursor.close()
        return aluno_id

    def editar(self, aluno_id: int, aluno: Dict[str, str]) -> None:
        cursor = self.mysql.connection.cursor()

        sql = "UPDATE aluno SET nome=%s WHERE idAluno=%s"
        values = (aluno['nome'], aluno_id)
        cursor.execute(sql, values)
        self.mysql.connection.commit()
        cursor.close()

    def editar_nota(self, idAluno, nota: Dict[str, str]) -> None:
        cursor = self.mysql.connection.cursor()
        sql = "UPDATE aluno SET nota=%s WHERE idAluno=%s"
        values = (nota['nota'], idAluno)
        cursor.execute(sql, values)
        self.mysql.connection.commit()
        cursor.close()

    def apagar(self, aluno_id: int) -> bool:
        cursor = self.mysql.connection.cursor()
        sql1 = "DELETE FROM aluno_avaliacao_360 WHERE idAluno = %s"
        cursor.execute(sql1, (aluno_id,))
        self.mysql.connection.commit()

        sql2 = "DELETE FROM avaliacao_360 WHERE idAvaliacao_360 IN (SELECT" \
               " idavaliacao_360 FROM aluno_avaliacao_360 WHERE idAluno = %s)"
        cursor.execute(sql2, (aluno_id,))
        self.mysql.connection.commit()

        sql3 = "DELETE FROM aluno_notas_gerais WHERE idAluno = %s"
        cursor.execute(sql3, (aluno_id,))
        self.mysql.connection.commit()

        sql4 = "DELETE FROM notas_gerais WHERE idnotas_gerais IN (SELECT" \
               " idnotas_gerais FROM aluno_notas_gerais WHERE idAluno = %s)"
        cursor.execute(sql4, (aluno_id,))
        self.mysql.connection.commit()

        sql5 = "DELETE FROM aluno WHERE idAluno = %s"
        cursor.execute(sql5, (aluno_id,))
        self.mysql.connection.commit()

        cursor.close()

    def calcula_gerais(self, notasGeraisAluno):
        somatorioNotasAvaliacaoObjetiva = 0
        somatorioNotasAvaliacaoDisertativa = 0
        somatorioNotasUas = 0
        somatorioNotasAvaliacaoEntregas = 0

        for nota in notasGeraisAluno:
            somatorioNotasAvaliacaoObjetiva = \
                somatorioNotasAvaliacaoObjetiva + (float(nota[0]) * 0.15)
            somatorioNotasAvaliacaoDisertativa = \
                somatorioNotasAvaliacaoDisertativa + (float(nota[1]) * 0.3)
            somatorioNotasUas = somatorioNotasUas + (float(nota[2]) * 0.1)
            somatorioNotasAvaliacaoEntregas = \
                somatorioNotasAvaliacaoEntregas + (float(nota[3]) * 0.15)

        try:
            somatorioNotasAvaliacaoObjetiva = \
                somatorioNotasAvaliacaoObjetiva / len(notasGeraisAluno)
        except ZeroDivisionError:
            somatorioNotasAvaliacaoObjetiva = 0
        try:
            somatorioNotasAvaliacaoDisertativa = \
                somatorioNotasAvaliacaoDisertativa / len(notasGeraisAluno)
        except ZeroDivisionError:
            somatorioNotasAvaliacaoDisertativa = 0
        try:
            somatorioNotasUas = somatorioNotasUas / len(notasGeraisAluno)
        except ZeroDivisionError:
            somatorioNotasUas = 0
        try:
            somatorioNotasAvaliacaoEntregas = \
                somatorioNotasAvaliacaoEntregas / len(notasGeraisAluno)
        except ZeroDivisionError:
            somatorioNotasAvaliacaoEntregas = 0

        return somatorioNotasAvaliacaoObjetiva + \
            somatorioNotasAvaliacaoDisertativa + somatorioNotasUas + \
            somatorioNotasAvaliacaoEntregas

    def calcula_360(self, notas360Aluno):
        somaEquipeComunicacao = 0
        somaEquipeCognitivo = 0
        somaEquipeAutogestao = 0
        somaEquipeAutonomia = 0
        somaEquipeProtagonismo = 0
        somaEquipeInteracao = 0

        somaAutoAvaliacaoComunicacao = 0
        somaAutoAvaliacaoCognitivo = 0
        somaAutoAvaliacaoAutogestao = 0
        somaAutoAvaliacaoAutonomia = 0
        somaAutoAvaliacaoProtagonismo = 0
        somaAutoAvaliacaoInteracao = 0

        somaProfessorComunicacao = 0
        somaProfessorCognitivo = 0
        somaProfessorAutogestao = 0
        somaProfessorAutonomia = 0
        somaProfessorProtagonismo = 0
        somaProfessorInteracao = 0

        contadorEquipe = 0
        contadorAutoAvaliacao = 0
        contadorProfessor = 0

        for nota in notas360Aluno:
            if (nota[0] == "Equipe"):
                somaEquipeComunicacao = somaEquipeComunicacao + \
                    (float(nota[1]) * 0.1)
                somaEquipeCognitivo = somaEquipeCognitivo + \
                    (float(nota[2]) * 0.1)
                somaEquipeAutogestao = somaEquipeAutogestao + \
                    (float(nota[3]) * 0.025)
                somaEquipeAutonomia = somaEquipeAutonomia + \
                    (float(nota[4]) * 0.025)
                somaEquipeProtagonismo = somaEquipeProtagonismo + \
                    (float(nota[5]) * 0.025)
                somaEquipeInteracao = somaEquipeInteracao + \
                    (float(nota[6]) * 0.025)
                contadorEquipe = contadorEquipe + 1

            if (nota[0] == "Professor"):
                somaProfessorComunicacao = somaProfessorComunicacao + \
                    (float(nota[1]) * 0.1)
                somaProfessorCognitivo = somaProfessorCognitivo + \
                    (float(nota[2]) * 0.1)
                somaProfessorAutogestao = somaProfessorAutogestao + \
                    (float(nota[3]) * 0.025)
                somaProfessorAutonomia = somaProfessorAutonomia + \
                    (float(nota[4]) * 0.025)
                somaProfessorProtagonismo = somaProfessorProtagonismo + \
                    (float(nota[5]) * 0.025)
                somaProfessorInteracao = somaProfessorInteracao + \
                    (float(nota[6]) * 0.025)
                contadorProfessor = contadorProfessor + 1

            if (nota[0] == "Auto Avaliação"):
                somaAutoAvaliacaoComunicacao = somaAutoAvaliacaoComunicacao + \
                    (float(nota[1]) * 0.1)
                somaAutoAvaliacaoCognitivo = somaAutoAvaliacaoCognitivo + \
                    (float(nota[2]) * 0.1)
                somaAutoAvaliacaoAutogestao = somaAutoAvaliacaoAutogestao + \
                    (float(nota[3]) * 0.025)
                somaAutoAvaliacaoAutonomia = somaAutoAvaliacaoAutonomia + \
                    (float(nota[4]) * 0.025)
                somaAutoAvaliacaoProtagonismo = \
                    somaAutoAvaliacaoProtagonismo + (float(nota[5]) * 0.025)
                somaAutoAvaliacaoInteracao = somaAutoAvaliacaoInteracao + \
                    (float(nota[6]) * 0.025)
                contadorAutoAvaliacao = contadorAutoAvaliacao + 1

        if contadorEquipe == 0:
            somaEquipe = 0
        else:
            somaEquipe = ((
                somaEquipeComunicacao + somaEquipeCognitivo +
                somaEquipeAutogestao + somaEquipeAutonomia +
                somaEquipeProtagonismo + somaEquipeInteracao) /
                          contadorEquipe) * 0.1

        if contadorAutoAvaliacao == 0:
            somaAutoAvalicao = 0
        else:
            somaAutoAvalicao = ((
                somaAutoAvaliacaoComunicacao + somaAutoAvaliacaoCognitivo +
                somaAutoAvaliacaoAutogestao + somaAutoAvaliacaoAutonomia +
                somaAutoAvaliacaoProtagonismo + somaAutoAvaliacaoInteracao) /
                contadorAutoAvaliacao) * 0.1

        if contadorProfessor == 0:
            somaProfessor = 0
        else:
            somaProfessor = ((
                somaProfessorComunicacao + somaProfessorCognitivo +
                somaProfessorAutogestao + somaProfessorAutonomia +
                somaProfessorProtagonismo + somaProfessorInteracao
            ) / contadorProfessor) * 0.8

        return somaAutoAvalicao + somaEquipe + somaProfessor

    def calcula_nota(self, notasGeraisAluno, notas360Aluno):
        notaGeral = self.calcula_gerais(notasGeraisAluno)
        nota360 = self.calcula_360(notas360Aluno)

        return notaGeral + nota360
