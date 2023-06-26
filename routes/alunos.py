# Importando os módulos necessários para o código
import os
from datetime import timedelta
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_mysqldb import MySQL

# Importando as classes necessárias para realizar a
# conexão com o banco de dados
from connection.aluno import Aluno
from connection.aluno_avaliacao_360 import AlunoAvaliacao360
from connection.aluno_notas_gerais import AlunoNotasGerais
from connection.avaliacao_360 import Avaliacao360
from connection.configuracoes import Configuracoes
from connection.notas_gerais import NotasGerais
from connection.tipo_avaliacao import TipoAvaliacao
from connection.turma import Turma
from connection.usuario import Usuario
# Importando a classe Arredondador que será utilizada no código
from utils.arredondador import Arredondador

# Criando a aplicação
app = Flask(__name__)

# Definindo uma chave secreta para a aplicação
app.secret_key = os.environ.get('SECRET_KEY')

# Inicializando o Bootstrap
Bootstrap(app)

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
turmaD = Turma(conexao)
usuario = Usuario(conexao)

# Instanciando a classe Arredondador
arredondador = Arredondador()


def professor_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_identity = get_jwt_identity()
        if user_identity and (
                user_identity["perfil"] == "professor" or
                user_identity["perfil"] == "admin"):
            return fn(*args, **kwargs)
        else:
            flash('Acesso negado: recurso disponível apenas para professores.',
                  'error')
            return redirect(url_for('home'))

    return wrapper


@app.route('/', methods=['GET', 'DELETE'])
@jwt_required()
def lista_alunos():
    return redirect(url_for('home'))


@app.route('/adicionar_aluno', methods=['GET', 'POST'])
@jwt_required()
@professor_required
def adicionar_aluno():
    if request.method == 'POST':
        nome = request.form['nome']
        if nome.strip() == '':
            flash('O nome do aluno não pode estar em branco.', 'error')
            return redirect(url_for('adicionar_aluno'))

        aluno_existente = aluno.buscar_aluno_por_nome(nome)
        if aluno_existente:
            flash('Já existe um aluno com esse nome.', 'error')
            return redirect(url_for('adicionar_aluno'))

        aluno.salvar({
            'nome': nome,
            'nota': '0',
        })
        flash('Aluno salvo com sucesso.', 'success')
        return redirect(url_for('gerenciar_alunos'))
    else:
        usuarios = aluno.usuarios_sem_alunos()
        turmas = turmaD.buscar_todos()
        return render_template('adicionar_aluno.html', usuarios=usuarios,
                               turmas=turmas)


@app.route('/deletar_aluno/<int:idAluno>', methods=['GET'])
@jwt_required()
@professor_required
def deletar_aluno(idAluno):
    aluno.apagar(idAluno)
    flash('Aluno deletado com sucesso.', 'warning')
    return redirect(url_for('gerenciar_alunos'))


@app.route('/editar_aluno/<int:idAluno>', methods=['GET', 'POST'])
@jwt_required()
@professor_required
def editar_aluno(idAluno):
    if request.method == 'GET':
        alunoBuscado = aluno.buscar_por_id(idAluno)
        return render_template('editar_aluno.html', aluno=alunoBuscado)

    elif request.method == 'POST':
        alunoBuscado = aluno.buscar_por_id(idAluno)
        nome = request.form['nome']

        if nome == alunoBuscado[1]:
            return redirect(url_for('gerenciar_alunos'))

        if nome.strip() == '':
            flash('O nome do aluno não pode estar em branco.', 'error')
            return redirect(url_for('editar_aluno', idAluno=idAluno))

        aluno_existente = aluno.buscar_aluno_por_nome(nome)
        if aluno_existente:
            flash('O nome do aluno já esta cadastrado.', 'error')
            return redirect(url_for('editar_aluno', idAluno=idAluno))

        aluno.editar(idAluno, {
            'nome': nome,
        })

        flash('Aluno salvo com sucesso.', 'succes')
        return redirect(url_for('gerenciar_alunos'))


@app.route('/gerenciar_alunos', methods=['GET'])
@jwt_required()
@professor_required
def gerenciar_alunos():
    alunos = aluno.buscar_todos_com_usuarios()
    return render_template('gerenciar_alunos.html', alunos=alunos)


@app.route('/vincular_usuario/<int:idAluno>', methods=['GET', 'POST'])
@jwt_required()
@professor_required
def vincular_usuario(idAluno):
    if request.method == 'POST':
        idusuario = request.form['idusuario']
        aluno.vincular_usuario(idAluno, idusuario)
        flash('Usuario vinculado com sucesso.', 'success')
        return redirect(url_for('gerenciar_alunos'))
    else:
        usuarios = usuario.buscar_aluno()
        return render_template('vincular_usuario.html', idAluno=idAluno,
                               usuarios=usuarios)


@app.route('/desvincular_usuario/<int:idAluno>', methods=['GET'])
@jwt_required()
@professor_required
def desvincular_usuario(idAluno):
    aluno.desvincular_usuario(idAluno)
    flash('Usuario desvinculado com sucesso.', 'success')
    return redirect(url_for('gerenciar_alunos'))
