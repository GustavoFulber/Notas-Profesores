# Importando os módulos necessários para o código
import os
from datetime import timedelta
from functools import wraps
from threading import Thread

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_mysqldb import MySQL

# Importando as classes necessárias para realizar a conexão
# com o banco de dados
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

emailSender = Email('smtp.hostinger.com', 465,
                    "notasprofessor@agendabpkedu.space", "Senha1@@@")


def enviar_email_assincrono(user, assunto, corpo):
    emailSender.enviarEmail(assunto, corpo, user[4])


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
usuarios = Usuario(conexao)

# Instanciando a classe Arredondador
arredondador = Arredondador()


def professor_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_identity = get_jwt_identity()
        if user_identity and (user_identity["perfil"] == "professor" or
           user_identity["perfil"] == "admin"):
            return fn(*args, **kwargs)
        else:
            flash('Acesso negado: recurso disponível apenas' +
                  'para professores.', 'error')
            return redirect(url_for('home'))

    return wrapper


@app.route('/adicionar_nota/<int:idAluno>/<int:idgrupo>/<int:idmateria>',
           methods=['GET', 'POST'])
@jwt_required()
@professor_required
def adicionar_nota(idAluno, idgrupo, idmateria):
    if request.method == 'POST':
        if not alunoNotasGerais.verificarNotaVazia(request):
            flash('Existe alguma nota em branco.', 'error')
            return redirect(
                url_for('adicionar_nota', idAluno=idAluno, idgrupo=idgrupo,
                        idmateria=idmateria))

        if not alunoNotasGerais.verificarNotaMaiorQueDez(request):
            flash('Existe alguma nota maior que 10.', 'error')
            return redirect(
                url_for('adicionar_nota', idAluno=idAluno, idgrupo=idgrupo,
                        idmateria=idmateria))

        idNotasGerais = notasGerais.inserir_notas_gerais({
            'avalicao_objetiva': float(request.form['avaliacao_objetiva']),
            'avaliacao_dissertativa': float(
                request.form['avaliacao_dissertativa']),
            'uas': float(request.form['uas']),
            'entregas': float(request.form['entregas']),
            'idmateria': idmateria
        })

        alunoNotasGerais.criar({
            'idAluno': idAluno,
            'idnotas_gerais': idNotasGerais,
        })

        arredonda = configuracoes.buscar_por_chave("Arredondamento")

        notasGeraisAluno = alunoNotasGerais.buscar_por_idAluno_materia(
            idAluno, idmateria)
        notas360Aluno = alunoAvaliacao360.buscar_por_idAluno_materia(
            idAluno, idmateria)

        nota = aluno.calcula_nota(notasGeraisAluno, notas360Aluno)

        nota = arredondador.arredondar(nota, arredonda[2])

        aluno.editar_nota(idAluno, {'nota': nota})

        alunoBuscado = aluno.buscar_por_id(idAluno)
        if alunoBuscado:
            idusuario = alunoBuscado[3]

            user = usuarios.buscar_por_id(idusuario)
            if user:
                Thread(target=enviar_email_assincrono,
                       args=(user, "Novas notas em seu boletim",
                             "Olá, há novas notas em seu boletim."
                             " Acesse o sistema em: <br>" +
                             "<a href = " + '"' +
                             "http://notasprofessor.tech/login" + '"' +
                             ">http://notasprofessor.tech/login</a>")).start()

        flash('Nota adicionada com sucesso.', 'success')
        return redirect(
            url_for('ver_alunos_grupo', grupo_id=idgrupo, idmateria=idmateria))
    else:
        return render_template('adicionar_nota.html', idAluno=idAluno,
                               idgrupo=idgrupo, idmateria=idmateria)


@app.route('/adicionar_nota_360/<int:idAluno>/<int:idgrupo>/<int:idmateria>',
           methods=['GET', 'POST'])
@jwt_required()
@professor_required
def adicionar_nota_360(idAluno, idgrupo, idmateria):
    if request.method == 'POST':
        if not alunoAvaliacao360.verificarNotaVazia(request):
            flash('Existe alguma nota em branco.', 'error')
            return redirect(
                url_for('adicionar_nota_360', idAluno=idAluno, idgrupo=idgrupo,
                        idmateria=idmateria))

        if not alunoAvaliacao360.verificarNotaMaiorQueDez(request):
            flash('Existe alguma nota maior que 10.', 'error')
            return redirect(
                url_for('adicionar_nota_360', idAluno=idAluno, idgrupo=idgrupo,
                        idmateria=idmateria))

        idAvaliacao = avaliacao360.salvar({
            'idtipo_avaliacao': int(request.form['idtipo_avaliacao']),
            'comunicacao': float(request.form['pComunicacao']),
            'cognitivo': float(request.form['pCognitivo']),
            'autogestao': float(request.form['pAutogestao']),
            'autonomia': float(request.form['pAutonomia']),
            'protagonismo': float(request.form['pProtagonismo']),
            'interacao': float(request.form['pInteracao']),
            'idmateria': idmateria
        })
        alunoAvaliacao360.salvar({
            'idAluno': idAluno,
            'idavaliacao_360': idAvaliacao,
        })

        alunoBuscado = aluno.buscar_por_id(idAluno)
        if alunoBuscado:
            idusuario = alunoBuscado[3]

            user = usuarios.buscar_por_id(idusuario)
            if user:
                Thread(target=enviar_email_assincrono,
                       args=(user, "Novas notas em seu boletim",
                             "Olá, há novas notas em seu boletim. Acesse o"
                             " sistema em: <br>" +
                             "<a href = " + '"' +
                             "http://notasprofessor.tech/login" + '"' +
                             ">http://notasprofessor.tech/login</a>")).start()

        flash('Nota salva com sucesso.', 'success')
        return redirect(
            url_for('ver_alunos_grupo', grupo_id=idgrupo, idmateria=idmateria))
    else:
        tipo_avaliacao = tipoAvaliacao.buscar_todos()
        return render_template('adicionar_nota_360.html', idAluno=idAluno,
                               tipo_avaliacao=tipo_avaliacao, idgrupo=idgrupo,
                               idmateria=idmateria)


@app.route('/detalhes/<int:idAluno>/<int:idgrupo>/<int:idmateria>',
           methods=['GET', 'DELETE'])
@jwt_required()
@professor_required
def detalhes(idAluno, idgrupo, idmateria):
    if request.method == 'DELETE':
        notas_gerais = alunoNotasGerais.buscar_por_idAluno_comid(idAluno,
                                                                 idmateria)

        avaliacao_360 = alunoAvaliacao360.buscar_por_idAluno_comid(idAluno,
                                                                   idmateria)

        flash('Deletado com sucesso.', 'warning')

        return render_template('detalhes.html', idAluno=idAluno,
                               notas_gerais=notas_gerais,
                               avaliacao_360=avaliacao_360, idgrupo=idgrupo,
                               idmateria=idmateria)
    else:
        notas_gerais = alunoNotasGerais.buscar_por_idAluno_comid(idAluno,
                                                                 idmateria)

        avaliacao_360 = alunoAvaliacao360.buscar_por_idAluno_comid(idAluno,
                                                                   idmateria)

        return render_template('detalhes.html', idAluno=idAluno,
                               notas_gerais=notas_gerais,
                               avaliacao_360=avaliacao_360, idgrupo=idgrupo,
                               idmateria=idmateria)


@app.route('/deletar_gerais/<int:idgerais>/<int:idgrupo>/<int:idmateria>',
           methods=['GET', 'DELETE'])
@jwt_required()
@professor_required
def deletar_gerais(idgerais, idgrupo, idmateria):
    if request.method == 'GET':
        idAluno = notasGerais.excluir_gerais(idgerais)

        request.method = 'GET'

        return redirect(url_for('detalhes', idAluno=idAluno, idgrupo=idgrupo,
                                idmateria=idmateria))
    else:
        idAluno = notasGerais.excluir_gerais(idgerais)
        flash('Avaliação deletado com sucesso.', 'warning')

        request.method = 'GET'

        return redirect(url_for('detalhes', idAluno=idAluno, idgrupo=idgrupo,
                                idmateria=idmateria))


@app.route('/editar_gerais/<int:idgerais>/<int:idgrupo>/<int:idmateria>',
           methods=['GET', 'POST'])
@jwt_required()
@professor_required
def editar_gerais(idgerais, idgrupo, idmateria):
    if request.method == 'POST':
        if not alunoNotasGerais.verificarNotaVazia(request):
            flash('Existe alguma nota em branco.', 'error')
            return redirect(
                url_for('editar_gerais', idgerais=idgerais, idgrupo=idgrupo,
                        idmateria=idmateria))

        if not alunoNotasGerais.verificarNotaMaiorQueDez(request):
            flash('Existe alguma nota maior que 10.', 'error')
            return redirect(
                url_for('editar_gerais', idgerais=idgerais, idgrupo=idgrupo,
                        idmateria=idmateria))

        idAluno = notasGerais.atualizar_notas_gerais(idgerais, {
            'avalicao_objetiva': float(request.form['avaliacao_objetiva']),
            'avaliacao_dissertativa': float(
                request.form['avaliacao_dissertativa']),
            'uas': float(request.form['uas']),
            'entregas': float(request.form['entregas'])
        })

        notasGeraisAluno = alunoNotasGerais.buscar_por_idAluno_materia(
            idAluno, idmateria)
        notas360Aluno = alunoAvaliacao360.buscar_por_idAluno_materia(
            idAluno, idmateria)

        nota = aluno.calcula_nota(notasGeraisAluno, notas360Aluno)

        arredonda = configuracoes.buscar_por_chave("Arredondamento")

        nota = arredondador.arredondar(nota, arredonda[2])

        aluno.editar_nota(idAluno, {'nota': nota})
        flash('Nota editada com sucesso.', 'success')
        return redirect(url_for('detalhes', idAluno=idAluno, idgrupo=idgrupo,
                                idmateria=idmateria))
    else:
        avaliacao = notasGerais.buscar_por_id(idgerais)

        idAluno = notasGerais.idAluno_por_gerais(idgerais)

        return render_template('editar_gerais.html', idgerais=idgerais,
                               avaliacao=avaliacao, idAluno=idAluno,
                               idgrupo=idgrupo, idmateria=idmateria)


@app.route('/deletar_360/<int:id360>/<int:idgrupo>/<int:idmateria>',
           methods=['GET', 'DELETE'])
@jwt_required()
@professor_required
def deletar_360(id360, idgrupo, idmateria):
    if request.method == 'GET':
        idAluno = avaliacao360.excluir_avaliacao360(id360)
        flash('Avaliação deletado com sucesso.', 'warning')

        return redirect(url_for('detalhes', idAluno=idAluno, idgrupo=idgrupo,
                                idmateria=idmateria))
    else:
        idAluno = avaliacao360.excluir_avaliacao360(id360)
        flash('Avaliação deletado com sucesso.', 'warning')

        notasGeraisAluno = alunoNotasGerais.buscar_por_idAluno(idAluno,
                                                               idmateria)
        notas360Aluno = alunoAvaliacao360.buscar_por_idAluno(idAluno,
                                                             idmateria)

        arredonda = configuracoes.buscar_por_chave("Arredondamento")

        nota = aluno.calcula_nota(notasGeraisAluno, notas360Aluno)

        nota = arredondador.arredondar(nota, arredonda[2])

        aluno.editar_nota(idAluno, {'nota': nota})

        return redirect(url_for('detalhes', idAluno=idAluno, idgrupo=idgrupo,
                                idmateria=idmateria))


@app.route('/editar_360/<int:id360>/<int:idgrupo>/<int:idmateria>',
           methods=['GET', 'POST'])
@jwt_required()
@professor_required
def editar_360(id360, idgrupo, idmateria):
    if request.method == 'POST':
        if not alunoAvaliacao360.verificarNotaVazia(request):
            flash('Existe alguma nota em branco.', 'error')
            return redirect(url_for('editar_360', id360=id360, idgrupo=idgrupo,
                                    idmateria=idmateria))

        if not alunoAvaliacao360.verificarNotaMaiorQueDez(request):
            flash('Existe alguma nota maior que 10.', 'error')
            return redirect(url_for('editar_360', id360=id360, idgrupo=idgrupo,
                                    idmateria=idmateria))

        idAluno = avaliacao360.editar(id360, {
            'idtipo_avaliacao': int(request.form['idtipo_avaliacao']),
            'comunicacao': float(request.form['pComunicacao']),
            'cognitivo': float(request.form['pCognitivo']),
            'autogestao': float(request.form['pAutogestao']),
            'autonomia': float(request.form['pAutonomia']),
            'protagonismo': float(request.form['pProtagonismo']),
            'interacao': float(request.form['pInteracao'])
        })

        flash('Nota editada com sucesso.', 'error')
        return redirect(url_for('detalhes', idAluno=idAluno, idgrupo=idgrupo,
                                idmateria=idmateria))
    else:
        tipo_avaliacao = tipoAvaliacao.buscar_todos()
        avaliacao = avaliacao360.buscar_por_id(id360)

        idAluno = avaliacao360.idAluno_por_360(id360)

        return render_template('editar_360.html', id360=id360,
                               tipo_avaliacao=tipo_avaliacao,
                               avaliacao=avaliacao, idAluno=idAluno,
                               idgrupo=idgrupo, idmateria=idmateria)


@app.route('/alterar_arredondamento/<int:idmateria>/<int:grupo_id>',
           methods=['POST'])
@jwt_required()
@professor_required
def alterar_arredondamento(idmateria, grupo_id):
    valor = request.form['valor']
    configuracoes.editar_por_chave("Arredondamento", valor)
    alunos = aluno.buscar_todos()

    arrendodamento = configuracoes.buscar_por_chave("Arredondamento")

    flash('Editado com sucesso.', 'success')
    return render_template('ver_alunos_grupo.html', alunos=alunos,
                           arrendodamento=arrendodamento, grupo_id=grupo_id,
                           idmateria=idmateria)
