import secrets

import bcrypt


class Usuario:
    def __init__(self, mySql):
        self.mysql = mySql

    def buscar_professores_admins(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM usuario WHERE perfil = 'professor' OR"
            " perfil = 'admin'")
        usuarios = cursor.fetchall()
        cursor.close()
        return usuarios

    def buscar_aluno(self):
        cursor = self.mysql.connection.cursor()
        sql = """
        SELECT usuario.*
        FROM usuario
        LEFT JOIN aluno ON usuario.idusuario = aluno.idusuario
        WHERE usuario.perfil = 'aluno' AND aluno.idusuario IS NULL
        """
        cursor.execute(sql)
        usuarios = cursor.fetchall()
        cursor.close()
        return usuarios

    def buscar_por_id(self, idusuario):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM usuario WHERE idusuario = %s", [idusuario])
        usuario = cur.fetchone()
        cur.close()
        return usuario

    def buscar_por_nome(self, nome):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM usuario WHERE usuario LIKE %s",
                    [f"%{nome}%"])
        usuarios = cur.fetchall()
        cur.close()
        return usuarios

    def editar(self, idusuario, usuario):
        cur = self.mysql.connection.cursor()
        cur.execute(
            "UPDATE usuario SET usuario = %s, senha = %s, email = %s"
            " WHERE idusuario = %s",
            (usuario['usuario'], usuario['senha'], usuario['email'], idusuario)
        )
        self.mysql.connection.commit()
        cur.close()

    def apagar(self, idusuario):
        cur = self.mysql.connection.cursor()
        cur.execute("DELETE FROM usuario WHERE idusuario = %s", [idusuario])
        self.mysql.connection.commit()
        cur.close()

    def aprovar_usuario(self, usuario_id):
        cur = self.mysql.connection.cursor()
        cur.execute(
            "UPDATE usuario SET aprovado = True, perfil = 'aluno'"
            " WHERE idusuario = %s",
            [usuario_id])
        self.mysql.connection.commit()
        cur.close()

    def get_total_usuarios(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuario")
        total_usuarios = cursor.fetchone()[0]
        cursor.close()
        return total_usuarios

    def get_total_avaliacoes_realizadas(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM avaliacao WHERE completo = TRUE")
        total_avaliacoes = cursor.fetchone()[0]
        cursor.close()
        return total_avaliacoes

    def login_nao_aprovado(self, credentials):
        cur = self.mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM usuario WHERE usuario = %s and aprovado = false",
            (credentials['usuario'],)
        )
        result = cur.fetchone()
        cur.close()

        if result and bcrypt.checkpw(credentials['senha'].encode('utf-8'),
                                     result[2].encode('utf-8')):
            return result
        else:
            return [False]

    def login(self, credentials):
        cur = self.mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM usuario WHERE usuario = %s and aprovado = true",
            (credentials['usuario'],)
        )
        result = cur.fetchone()
        cur.close()

        if result and bcrypt.checkpw(credentials['senha'].encode('utf-8'),
                                     result[2].encode('utf-8')):
            return result
        else:
            return [False]

    def editar_perfil(self, usuario_id, perfil):
        cur = self.mysql.connection.cursor()
        cur.execute("UPDATE usuario SET perfil = %s WHERE idusuario = %s",
                    (perfil, usuario_id))
        self.mysql.connection.commit()
        cur.close()

    def registro(self, registroUsuario):

        cur = self.mysql.connection.cursor()

        codigo = ""

        while codigo == "":
            for _ in range(7):
                digito = secrets.randbelow(10)
                codigo += str(digito)

            cur.execute("SELECT * FROM usuario WHERE codigo = %s", (codigo,))
            resultado = cur.fetchone()

            if resultado:
                codigo = ""

        cur.execute("SELECT * FROM usuario WHERE usuario = %s OR email = %s",
                    (registroUsuario['usuario'], registroUsuario['email']))
        resultado = cur.fetchone()
        if resultado:
            return 'Erro: Nome de usuário ou endereço de e-mail já cadastrado'

        cur.execute(
            "INSERT INTO usuario (usuario, email, nome, codigo) VALUES"
            " (%s, %s, %s, %s)",
            (registroUsuario['usuario'], registroUsuario['email'],
             registroUsuario['nome'], codigo))
        self.mysql.connection.commit()
        cur.close()

        return codigo

    def salvarSenha(self, verificar):

        cur = self.mysql.connection.cursor()

        cur.execute("SELECT * FROM usuario WHERE usuario = %s AND codigo = %s",
                    (verificar['usuario'], verificar['codigo']))
        resultado = cur.fetchone()
        if not resultado:
            return False

        hashed_senha = bcrypt.hashpw(verificar['password'].encode('utf-8'),
                                     bcrypt.gensalt())

        cur.execute(
            "UPDATE usuario SET senha = %s, codigo = null, verificado"
            " = %s WHERE idusuario = %s",
            (hashed_senha, True, resultado[0]))
        self.mysql.connection.commit()
        cur.close()
        return True

    def recuperar_senha(self, email):
        cur = self.mysql.connection.cursor()

        cur.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        usuario = cur.fetchone()

        if not usuario:
            return "Erro: Email não encontratado"

        codigo = ""

        while codigo == "":
            for _ in range(7):
                digito = secrets.randbelow(10)
                codigo += str(digito)

            cur.execute("SELECT * FROM usuario WHERE codigo = %s", (codigo,))
            resultado = cur.fetchone()

            if resultado:
                codigo = ""

        cur.execute("UPDATE usuario SET codigo = %s WHERE email = %s",
                    (codigo, email))
        self.mysql.connection.commit()

        return codigo

    def redefinir_senha(self, user_id, email, nova_senha):
        cur = self.mysql.connection.cursor()

        cur.execute("SELECT * FROM usuario WHERE idusuario = %s", (user_id,))
        resultado = cur.fetchone()

        if not resultado or resultado[4] != email:
            return False

        hashed_senha = bcrypt.hashpw(nova_senha.encode('utf-8'),
                                     bcrypt.gensalt())

        cur.execute("UPDATE usuario SET senha = %s WHERE idusuario = %s",
                    (hashed_senha, user_id))
        self.mysql.connection.commit()
        cur.close()

        return True

    def buscar_usuarios_verificados(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM usuario WHERE verificado = True")
        resultado = cur.fetchall()
        cur.close()
        return resultado
