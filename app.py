# -*- coding: utf-8 -*-
# Importando os módulos necessários para o código
import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_mysqldb import MySQL

# Importing the necessary classes to connect with the database
from connection.aluno import Aluno
from connection.aluno_avaliacao_360 import AlunoAvaliacao360
from connection.aluno_notas_gerais import AlunoNotasGerais
from connection.avaliacao_360 import Avaliacao360
from connection.configuracoes import Configuracoes
from connection.notas_gerais import NotasGerais
from connection.tipo_avaliacao import TipoAvaliacao
# Importing the routes that will be used in the code
from routes.alunos import (adicionar_aluno, deletar_aluno, desvincular_usuario,
                           editar_aluno, gerenciar_alunos, lista_alunos,
                           vincular_usuario)
from routes.configuracoes import (adicionar_grupo, adicionar_materia,
                                  adicionar_turma, criar_autoavaliacao,
                                  criar_avaliacao_grupo, deletar_grupo,
                                  deletar_materia, deletar_turma, editar_grupo,
                                  editar_materia, editar_turma, grupo, materia,
                                  minhas_avaliacoes, minhas_notas,
                                  realizar_avaliacao, remover_aluno,
                                  remover_aluno_grupo, turma, ver_alunos,
                                  ver_alunos_grupo, ver_notas_detalhadas,
                                  vincular_aluno, vincular_aluno_grupo)
from routes.notas import (adicionar_nota, adicionar_nota_360,
                          alterar_arredondamento, deletar_360, deletar_gerais,
                          detalhes, editar_360, editar_gerais)
from routes.usuario import (aprovar_usuario, dashboard, editar_usuario,
                            esqueci_senha, excluir_usuario, home,
                            lista_usuario, login, logout, mudar_senha,
                            registro_usuario, verificar_codigo)
# Importing the Arredondador class that will be used in the code
from utils.arredondador import Arredondador
from utils.perfil import custom_template_context, perfil

# Criando a aplicação
app = Flask(__name__)

if os.getenv('FLASK_ENV') == 'production':
    load_dotenv("production.env")
else:
    load_dotenv("development.env")

# Definindo uma chave secreta para a aplicação
app.secret_key = os.getenv('SECRET_KEY')

# Inicializando o Bootstrap
Bootstrap(app)

app.jinja_env.globals["user_perfil"] = perfil
app.context_processor(custom_template_context)

# Configurando o banco de dados
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=125)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['PORT'] = int(os.getenv('PORT'))
app.config['HOST'] = os.getenv('HOST')

jwt = JWTManager(app)

# Conectando-se ao banco de dados
conexao = MySQL(app)

# Instanciando as classes necessárias para o código
aluno = Aluno(conexao)
tipoAvaliacao = TipoAvaliacao(conexao)
avaliacao360 = Avaliacao360(conexao)
alunoAvaliacao360 = AlunoAvaliacao360(conexao)
notasGerais = NotasGerais(conexao)
alunoNotasGerais = AlunoNotasGerais(conexao)
configuracoes = Configuracoes(conexao)

# Instanciando a classe Arredondador
arredondador = Arredondador()


@app.errorhandler(NoAuthorizationError)
def handle_no_auth_error(e):
    return redirect(url_for('login'))


# Definindo as rotas da aplicação
# Rota para listar os alunos cadastrados no banco de dados
app.route('/', methods=['GET', 'DELETE'])(lista_alunos)

# Rota para adicionar um aluno ao banco de dados
app.route('/adicionar_aluno', methods=['GET', 'POST'])(adicionar_aluno)

app.route('/deletar_aluno/<int:idAluno>',
          methods=['GET'])(
    deletar_aluno)  # Rota para deletar um aluno do banco de dados

# Rota para editar as informações de um aluno cadastrado no banco de dados
app.route('/editar_aluno/<int:idAluno>',
          methods=['GET', 'POST'])(editar_aluno)

app.route('/adicionar_nota/<int:idAluno>/<int:idgrupo>/<int:idmateria>',
          methods=['GET', 'POST'])(
    adicionar_nota)  # Rota para adicionar uma nota ao aluno

app.route('/adicionar_nota_360/<int:idAluno>/<int:idgrupo>/<int:idmateria>',
          methods=['GET', 'POST'])(
    adicionar_nota_360)  # Rota para adicionar uma avaliação 360º ao aluno

# Rota para visualizar os detalhes de um aluno cadastrado no banco de dados
app.route('/detalhes/<int:idAluno>/<int:idgrupo>/<int:idmateria>',
          methods=['GET', 'DELETE'])(detalhes)

# Rota para deletar uma nota geral do aluno
app.route('/deletar_gerais/<int:idgerais>/<int:idgrupo>/<int:idmateria>',
          methods=['GET', 'DELETE'])(deletar_gerais)

# Rota para editar uma nota geral do aluno
app.route('/editar_gerais/<int:idgerais>/<int:idgrupo>/<int:idmateria>',
          methods=['GET', 'POST'])(editar_gerais)

# Rota para deletar uma avaliação 360º do aluno
app.route('/deletar_360/<int:id360>/<int:idgrupo>/<int:idmateria>',
          methods=['GET', 'DELETE'])(deletar_360)

# Rota para editar uma avaliação 360º do aluno
app.route('/editar_360/<int:id360>/<int:idgrupo>/<int:idmateria>',
          methods=['GET', 'POST'])(editar_360)

# Rota para alterar a configuração de arredondamento de notas
app.route('/alterar_arredondamento/<int:idmateria>/<int:grupo_id>',
          methods=['POST'])(alterar_arredondamento)

# Rota para fazer o login
app.route('/login', methods=['POST', 'GET'])(login)

# Rota de registro
app.route('/registro_usuario', methods=['POST', 'GET'])(registro_usuario)

# Rota de verificar codigo de cadastro
app.route('/verificar_codigo', methods=['POST', 'GET'])(verificar_codigo)

# Rota de logout
app.route('/logout', methods=['GET'])(logout)

# Rota de home
app.route('/home', methods=['GET'])(home)

# Rota de dashboard
app.route('/dashboard', methods=['GET'])(dashboard)

app.route('/esqueci_senha', methods=['GET', 'POST'])(esqueci_senha)

app.route('/mudar_senha', methods=['GET', 'POST'])(mudar_senha)

app.route('/lista_usuario', methods=['GET', 'POST'])(lista_usuario)

app.route('/aprovar_usuario/<int:usuario_id>',
          methods=['GET'])(aprovar_usuario)

app.route('/excluir_usuario/<int:usuario_id>',
          methods=['GET'])(excluir_usuario)

app.route('/editar_usuario/<int:usuario_id>',
          methods=['GET', 'POST'])(editar_usuario)

app.route('/materia', methods=['GET'])(materia)

app.route('/turma', methods=['GET'])(turma)

app.route('/grupo/<int:materia_id>', methods=['GET'])(grupo)

app.route('/adicionar_materia', methods=['GET', 'POST'])(adicionar_materia)

app.route('/adicionar_turma', methods=['GET', 'POST'])(adicionar_turma)

app.route('/adicionar_grupo/<int:materia_id>',
          methods=['GET', 'POST'])(adicionar_grupo)

app.route('/editar_materia/<int:materia_id>',
          methods=['GET', 'POST'])(editar_materia)

app.route('/editar_turma/<int:turma_id>',
          methods=['GET', 'POST'])(editar_turma)

app.route('/editar_grupo/<int:grupo_id>',
          methods=['GET', 'POST'])(editar_grupo)

app.route('/deletar_materia/<int:materia_id>',
          methods=['GET'])(deletar_materia)

app.route('/deletar_turma/<int:turma_id>', methods=['GET'])(deletar_turma)

app.route('/deletar_grupo/<int:grupo_id>', methods=['GET'])(deletar_grupo)

app.route('/turma/<int:turma_id>/vincular_aluno',
          methods=['GET', 'POST'])(vincular_aluno)

app.route('/turma/<int:turma_id>/remover_aluno',
          methods=['GET', 'POST'])(remover_aluno)

app.route('/turma/<int:turma_id>/ver_alunos', methods=['GET'])(ver_alunos)

app.route('/vincular_aluno_grupo/<int:grupo_id>/<int:idmateria>',
          methods=['GET', 'POST'])(vincular_aluno_grupo)

app.route('/remover_aluno_grupo/<int:grupo_id>/<int:idmateria>',
          methods=['GET', 'POST'])(remover_aluno_grupo)

app.route('/ver_alunos_grupo/<int:grupo_id>/<int:idmateria>',
          methods=['GET'])(ver_alunos_grupo)

app.route('/criar_autoavaliacao//<int:idmateria>',
          methods=['GET'])(criar_autoavaliacao)

app.route('/criar_avaliacao_grupo/<int:idmateria>',
          methods=['GET'])(criar_avaliacao_grupo)

app.route('/minhas_avaliacoes', methods=['GET'])(minhas_avaliacoes)

app.route('/realizar_avaliacao/<int:idavaliacao>',
          methods=['GET', 'POST'])(realizar_avaliacao)

app.route('/minhas_notas', methods=['GET'])(minhas_notas)

app.route('/ver_notas_detalhadas/<int:idmateria>',
          methods=['GET'])(ver_notas_detalhadas)

app.route('/gerenciar_alunos', methods=['GET'])(gerenciar_alunos)

app.route('/vincular_usuario/<int:idAluno>',
          methods=['POST', 'GET'])(vincular_usuario)

app.route('/desvincular_usuario/<int:idAluno>',
          methods=['GET'])(desvincular_usuario)

# Inicializando a aplicação
app.run(
        port=app.config['PORT'],
        host=app.config['HOST'],
        debug=os.getenv('FLASK_DEBUG', False)
        )
