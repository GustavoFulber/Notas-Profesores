# Importando os módulos necessários para o código
import os
from datetime import timedelta
from functools import wraps

from flask import (Flask, flash, make_response, redirect, render_template,
                   request, url_for)
from flask_bootstrap import Bootstrap
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required,
                                set_access_cookies)
from flask_mysqldb import MySQL

# Importando as classes necessárias para realizar a
# conexão com o banco de dados
from connection.aluno import Aluno
from connection.aluno_avaliacao_360 import AlunoAvaliacao360
from connection.aluno_notas_gerais import AlunoNotasGerais
from connection.avaliacao_360 import Avaliacao360
from connection.configuracoes import Configuracoes
from connection.email import Email
from connection.notas_gerais import NotasGerais
from connection.tipo_avaliacao import TipoAvaliacao
from connection.usuario import Usuario
# Importando a classe Arredondador que será utilizada no código
from utils.arredondador import Arredondador
from utils.calcula_grafico import Calcula_grafico

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
usuario = Usuario(conexao)

emailSender = Email('smtp.hostinger.com', 465,
                    "notasprofessor@agendabpkedu.space", "Senha1@@@")

# Instanciando a classe Arredondador
arredondador = Arredondador()
calculaGrafico = Calcula_grafico()


def professor_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_identity = get_jwt_identity()
        if user_identity and (
                user_identity["perfil"] == "professor" or user_identity[
                "perfil"] == "admin"
                ):
            return fn(*args, **kwargs)
        else:
            flash('Acesso negado: recurso disponível apenas para professores.',
                  'error')
            return redirect(url_for('home'))

    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_identity = get_jwt_identity()
        if user_identity and user_identity["perfil"] == "admin":
            return fn(*args, **kwargs)
        else:
            flash(
                'Acesso negado: recurso disponível'
                ' apenas para administradores.',
                'error')
            return redirect(url_for('home'))

    return wrapper


@app.route('/lista_usuario', methods=['GET', 'POST'])
@jwt_required()
@professor_required
def lista_usuario():
    usuarios = usuario.buscar_usuarios_verificados()
    return render_template('lista_usuario.html', usuarios=usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuarioForm = request.form['username']
        senha = request.form['password']
        credentials = {'usuario': usuarioForm, 'senha': senha}

        user_nao = usuario.login_nao_aprovado(credentials)
        if user_nao[0]:
            return render_template("sem_autenticacao.html")

        user_id = usuario.login(credentials)

        if user_id[0]:
            flash('Login bem-sucedido!', 'success')
            user_identity = {"id": user_id[0], "perfil": user_id[6]}
            access_token = create_access_token(identity=user_identity)
            resp = make_response(redirect(url_for('home')))
            set_access_cookies(resp, access_token)
            return resp
        else:
            flash('Usuário ou senha inválidos!', 'error')
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/aprovar_usuario/<int:usuario_id>', methods=['GET'])
@jwt_required()
@professor_required
def aprovar_usuario(usuario_id):
    usuario.aprovar_usuario(usuario_id)
    flash("Usuário aprovado com sucesso!", "success")
    user = usuario.buscar_por_id(usuario_id)
    emailSender.enviarEmail("Acesso Liberado",
                            "Olá, seu cadastro foi aprovado, agora você"
                            " tem acesso ao sistema em: <br>" +
                            "<a href = " + '"' +
                            "http://notasprofessor.tech/verificar_codigo" +
                            '"' +
                            ">http://notasprofessor.tech/login</a>", user[4])
    return redirect(url_for('lista_usuario'))


@app.route('/editar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
@jwt_required()
@admin_required
def editar_usuario(usuario_id):
    if request.method == 'POST':
        if 'perfil' in request.form:
            perfil = request.form['perfil']
            usuario.editar_perfil(usuario_id, perfil)
            flash("Perfil atualizado com sucesso!", "success")
            return redirect(url_for('lista_usuario'))
        else:
            flash("Perfil não encontrado", "error")

    usuario_atual = usuario.buscar_por_id(usuario_id)
    return render_template('editar_usuario.html', usuario=usuario_atual)


@app.route('/excluir_usuario/<int:usuario_id>', methods=['GET'])
@jwt_required()
@professor_required
def excluir_usuario(usuario_id):
    user = usuario.buscar_por_id(usuario_id)
    usuario.apagar(usuario_id)
    flash("Usuário excluído com sucesso!", "warning")
    emailSender.enviarEmail("Acesso Negado",
                            "Olá, seu cadastro foi rejeitado ou excluido"
                            " por um administrador <br>" +
                            "Entre em contato com a secretaria"
                            " para ter mais informações",
                            user[4])
    return redirect(url_for('lista_usuario'))


@app.route('/registro_usuario', methods=['GET', 'POST'])
def registro_usuario():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']

        if ' ' in username:
            error = 'O nome de usuário não pode ter espaços'
            return render_template('registro_usuario.html', error=error)

        retorno = usuario.registro({
            "nome": name,
            "email": email,
            "usuario": username})

        if "Erro:" in retorno:
            flash(retorno, 'error')
            error = 'Ouve problemas de conexão com o servidor'
            return render_template('registro_usuario.html', error=error)

        flash("Um codigo de verificação foi enviado para o seu e-mail.",
              'success')

        emailSender.enviarEmail("Codigo",
                                "Olá <h4>" + name + "</h4><br>Codigo de"
                                " verificação: <h1>" + retorno + "</h1>" +
                                "<br> Conclua seu cadastro em <a href=" + '"' +
                                "http://notasprofessor.tech/verificar_codigo" +
                                '"' +
                                ">http://notasprofessor.tech/verificar_codigo"
                                "</a>",
                                email)

        return redirect(url_for('verificar_codigo'))

    return render_template('registro_usuario.html')


@app.route('/esqueci_senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        email = request.form['email']

        retorno = usuario.recuperar_senha(email)

        if "Erro:" in retorno:
            flash(retorno, 'error')
            error = 'Email não encontratado'
            return render_template('esqueci_senha.html', error=error)

        flash("Um codigo de verificação foi enviado para o seu e-mail.",
              'success')

        emailSender.enviarEmail("Codigo",
                                "Olá, <br>Codigo de verificação: <h1>" +
                                retorno + "</h1>" +
                                "<br> Troque sua senha em <a href=" + '"' +
                                "http://notasprofessor.tech/verificar_codigo" +
                                '"' +
                                ">http://notasprofessor.tech/verificar_codigo"
                                "</a>",
                                email)

        return redirect(url_for('verificar_codigo'))

    return render_template('esqueci_senha.html')


@app.route('/verificar_codigo', methods=['GET', 'POST'])
def verificar_codigo():
    if request.method == 'POST':
        usuarioForm = request.form['usuario']
        codigo = request.form['codigo']
        password = request.form['password']
        confirmar_password = request.form['confirmar_password']

        if password != confirmar_password:
            error = 'Senhas são diferentes'
            return render_template('verificar_codigo.html', error=error)

        retorno = usuario.salvarSenha({
            "usuario": usuarioForm,
            "codigo": codigo,
            "password": password})

        if not retorno:
            error = 'Codigo ou usuario incorreto'
            return render_template('verificar_codigo.html', error=error)
        flash(
            "Cadastro finalizado, aguarde alguém aceita-lo,"
            " você recebera um email",
            'success')

        user = usuario.buscar_por_nome(usuarioForm)

        aluno.salvar({
            'nome': user[0][3],
            'nota': '0',
            'usuario': user[0][0]
        })
        return redirect(url_for('login'))

    return render_template('verificar_codigo.html')


@app.route('/logout')
def logout():
    resp = make_response(redirect('/login'))
    resp.set_cookie('access_token_cookie', '', expires=0)
    return resp


@app.route('/home')
@jwt_required()
def home():
    total_usuarios = usuario.get_total_usuarios()
    total_avaliacoes_realizadas = usuario.get_total_avaliacoes_realizadas()

    notas_gerais = aluno.get_notas_gerais()

    charts_data = [
        Calcula_grafico.process_grades([item[1] for item in notas_gerais]),
        Calcula_grafico.process_grades([item[2] for item in notas_gerais]),
        Calcula_grafico.process_grades([item[4] for item in notas_gerais]),
        Calcula_grafico.process_grades([item[3] for item in notas_gerais]),
    ] if notas_gerais else []

    chart_titles = [
        "Notas Avaliação Objetiva",
        "Notas Avaliaçao Dissertativa",
        "Notas UAs",
        "Notas Entrega Final",
    ] if notas_gerais else []

    return render_template(
        'home.html', total_usuarios=total_usuarios,
        total_avaliacoes_realizadas=total_avaliacoes_realizadas,
        chart_titles=chart_titles, charts_data=charts_data)


@app.route('/dashboard')
@jwt_required()
def dashboard():
    notas_finais = aluno.get_notas_finais()
    notas_gerais = aluno.get_notas_gerais()
    avaliacao_360 = aluno.get_avaliacao_360()

    charts_data = [
        Calcula_grafico.process_grades([item[0] for item in notas_finais]),
        Calcula_grafico.process_grades([item[1] for item in notas_gerais]),
        Calcula_grafico.process_grades([item[2] for item in notas_gerais]),
        Calcula_grafico.process_grades([item[4] for item in notas_gerais]),
        Calcula_grafico.process_grades([item[3] for item in notas_gerais]),
        Calcula_grafico.process_grades(
            [Calcula_grafico.calcula360(item[:-2]) for item in avaliacao_360 if
             item[-2] == 2]),
        Calcula_grafico.process_grades(
            [Calcula_grafico.calcula360(item[:-2]) for item in avaliacao_360 if
             item[-2] == 3]),
        Calcula_grafico.process_grades(
            [Calcula_grafico.calcula360(item[:-2]) for item in avaliacao_360 if
             item[-2] == 1])
    ]

    chart_titles = [
        "Notas Finais",
        "Notas Avaliação Objetiva",
        "Notas Avaliaçao Dissertativa",
        "Notas UAs",
        "Notas Entrega Final",
        "Notas Professor",
        "Notas Equipe",
        "Notas Auto Avaliação",
    ]

    return render_template('dashboard.html', charts_data=charts_data,
                           chart_titles=chart_titles)


@app.route('/mudar_senha', methods=['GET', 'POST'])
@jwt_required()
def mudar_senha():
    user_identity = get_jwt_identity()
    user_id = user_identity["id"]
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        if senha != confirmar_senha:
            flash(
                "Erro: As senhas não são iguais. Por favor, tente novamente.",
                "error")
        else:
            resultado = usuario.redefinir_senha(user_id, email, senha)

            if resultado:
                flash("Senha alterada com sucesso!", "sucess")
            else:
                flash(
                    "Não foi possível alterar a senha. Verifique o"
                    " email informado.",
                    "error")

        return redirect('/mudar_senha')

    return render_template('mudar_senha.html')
