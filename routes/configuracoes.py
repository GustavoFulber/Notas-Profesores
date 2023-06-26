# Importando os módulos necessários para o código
import os
from datetime import timedelta
from functools import wraps
from threading import Thread

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
from connection.email import Email
from connection.grupo import Grupo
from connection.materia import Materia
from connection.notas_gerais import NotasGerais
from connection.tipo_avaliacao import TipoAvaliacao
from connection.turma import Turma
from connection.usuario import Usuario
from utils.arredondador import Arredondador

emailSender = Email('smtp.hostinger.com', 465,
                    "notasprofessor@agendabpkedu.space",
                    "Senha1@@@")


def enviar_email_assincrono(user, assunto, corpo):
    emailSender.enviarEmail(assunto, corpo, user[4])


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
alunoDAO = Aluno(conexao)
tipoAvaliacao = TipoAvaliacao(conexao)
avaliacao360 = Avaliacao360(conexao)
alunoAvaliacao360 = AlunoAvaliacao360(conexao)
notasGerais = NotasGerais(conexao)
alunoNotasGerais = AlunoNotasGerais(conexao)
turmaD = Turma(conexao)
materiaD = Materia(conexao)
configuracoes = Configuracoes(conexao)
usuarios = Usuario(conexao)
grupoD = Grupo(conexao)
alunoAvaliacao360 = AlunoAvaliacao360(conexao)

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


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_identity = get_jwt_identity()
        if user_identity and user_identity["perfil"] == "admin":
            return fn(*args, **kwargs)
        else:
            flash(
                'Acesso negado: recurso disponível apenas para'
                ' administradores.',
                'error')
            return redirect(url_for('home'))

    return wrapper


@app.route('/materia')
@jwt_required()
@professor_required
def materia():
    user_identity = get_jwt_identity()
    perfil = user_identity["perfil"]
    usuarioId = user_identity["id"]
    materias = materiaD.buscar_todas(usuarioId, perfil)
    return render_template('materia.html', materias=materias, perfil=perfil)


@app.route('/turma')
@jwt_required()
@admin_required
def turma():
    turmas = turmaD.buscar_todos()
    return render_template('turma.html', turmas=turmas)


@app.route('/grupo/<int:materia_id>')
@jwt_required()
@professor_required
def grupo(materia_id):
    grupos = grupoD.buscar_por_materia(materia_id)
    materia = materiaD.buscar_por_id(materia_id)
    return render_template('grupo.html', grupos=grupos, materia=materia)


@app.route('/adicionar_materia', methods=['GET', 'POST'])
@jwt_required()
@professor_required
def adicionar_materia():
    if request.method == 'POST':
        nome = request.form['nome']
        idresponsavel = request.form['idresponsavel']
        idturma = request.form['idturma']
        materiaD.adicionar_materia(nome, idresponsavel, idturma)
        flash('Matéria salva com sucesso.', 'success')
        return redirect(url_for('materia'))
    responsaveis = usuarios.buscar_professores_admins()
    turmas = turmaD.buscar_todos()
    return render_template('adicionar_materia.html', responsaveis=responsaveis,
                           turmas=turmas)


@app.route('/adicionar_turma', methods=['GET', 'POST'])
@jwt_required()
@admin_required
def adicionar_turma():
    if request.method == 'POST':
        nome = request.form['nome']
        periodo = request.form['periodo']
        turmaD.adicionar_turma(nome, periodo)
        flash('Turma salva com sucesso.', 'success')
        return redirect(url_for('turma'))
    return render_template('adicionar_turma.html')


@app.route('/adicionar_grupo/<int:materia_id>', methods=['GET', 'POST'])
@jwt_required()
@professor_required
def adicionar_grupo(materia_id):
    if request.method == 'POST':
        nome = request.form['nome']
        grupoD.adicionar_grupo(nome, materia_id)
        flash('Grupo salvo com sucesso.', 'success')
        return redirect(url_for('grupo', materia_id=materia_id))
    return render_template('adicionar_grupo.html', materia_id=materia_id)


@app.route('/editar_materia/<int:materia_id>', methods=['GET', 'POST'])
@jwt_required()
@professor_required
def editar_materia(materia_id):
    if request.method == 'POST':
        nome = request.form['nome']
        idresponsavel = request.form['idresponsavel']
        idturma = request.form['idturma']
        materiaD.editar_materia(materia_id, nome, idresponsavel, idturma)
        flash('Matéria salva com sucesso.', 'success')
        return redirect(url_for('materia'))
    materia = materiaD.buscar_por_id(materia_id)
    responsaveis = usuarios.buscar_professores_admins()
    turmas = turmaD.buscar_todos()
    return render_template('editar_materia.html', materia=materia,
                           responsaveis=responsaveis, turmas=turmas)


@app.route('/editar_turma/<int:turma_id>', methods=['GET', 'POST'])
@jwt_required()
@admin_required
def editar_turma(turma_id):
    if request.method == 'POST':
        nome = request.form['nome']
        periodo = request.form['periodo']
        turmaD.editar_turma(turma_id, nome, periodo)
        flash('Turma salva com sucesso.', 'success')
        return redirect(url_for('turma'))

    turma = turmaD.buscar_por_id(turma_id)
    return render_template('editar_turma.html', turma=turma)


@app.route('/editar_grupo/<int:grupo_id>', methods=['GET', 'POST'])
@jwt_required()
@professor_required
def editar_grupo(grupo_id):
    if request.method == 'POST':
        nome = request.form['nome']
        grupoD.editar_grupo(grupo_id, nome)
        grupo = grupoD.buscar_por_id(grupo_id)
        flash('Grupo salvo com sucesso.', 'success')
        print(grupo[2])
        return redirect(url_for('grupo', materia_id=grupo[2]))
    grupo = grupoD.buscar_por_id(grupo_id)
    return render_template('editar_grupo.html', grupo=grupo)


@app.route('/deletar_materia/<int:materia_id>', methods=['GET'])
@jwt_required()
@professor_required
def deletar_materia(materia_id):
    materiaD.deletar_materia(materia_id)
    flash('Matéria deletada com sucesso.', 'warning')
    return redirect(url_for('materia'))


@app.route('/deletar_turma/<int:turma_id>', methods=['GET'])
@jwt_required()
@admin_required
def deletar_turma(turma_id):
    turmaD.deletar_turma(turma_id)
    flash('Turma deletada com sucesso.', 'warning')
    return redirect(url_for('turma'))


@app.route('/deletar_grupo/<int:grupo_id>', methods=['GET'])
@jwt_required()
@professor_required
def deletar_grupo(grupo_id):
    grupo = grupoD.buscar_por_id(grupo_id)
    grupoD.deletar_grupo(grupo_id)
    flash('Grupo deletado com sucesso.', 'warning')
    return redirect(url_for('grupo', materia_id=grupo[2]))


@app.route('/turma/<int:turma_id>/vincular_aluno', methods=['GET', 'POST'])
@jwt_required()
@admin_required
def vincular_aluno(turma_id):
    if request.method == 'POST':
        aluno_id = request.form['aluno']
        turmaD.vincular_aluno(turma_id, aluno_id)
        flash('Aluno vinculado com sucesso!', 'success')
        return redirect(url_for('turma'))
    else:
        alunos = turmaD.listar_alunos_nao_vinculados(turma_id)
        return render_template('vincular_aluno.html', turma_id=turma_id,
                               alunos=alunos)


@app.route('/turma/<int:turma_id>/remover_aluno', methods=['GET', 'POST'])
@jwt_required()
@admin_required
def remover_aluno(turma_id):
    if request.method == 'POST':
        aluno_id = request.form['aluno']
        turmaD.remover_aluno(turma_id, aluno_id)
        flash('Aluno removido com sucesso!', 'success')
        return redirect(url_for('turma'))
    else:
        alunos = turmaD.listar_alunos_vinculados(turma_id)
        return render_template('remover_aluno.html', turma_id=turma_id,
                               alunos=alunos)


@app.route('/turma/<int:turma_id>/ver_alunos', methods=['GET'])
@jwt_required()
@admin_required
def ver_alunos(turma_id):
    alunos = turmaD.listar_alunos_vinculados(turma_id)
    return render_template('ver_alunos.html', turma_id=turma_id, alunos=alunos)


@app.route('/vincular_aluno_grupo/<int:grupo_id>/<int:idmateria>',
           methods=['GET', 'POST'])
@jwt_required()
@professor_required
def vincular_aluno_grupo(grupo_id, idmateria):
    if request.method == 'POST':
        aluno_id = request.form['aluno']
        grupoD.vincular_aluno(grupo_id, aluno_id)
        flash('Aluno vinculado ao grupo com sucesso!', 'success')
        return redirect(
            url_for('ver_alunos_grupo', grupo_id=grupo_id,
                    idmateria=idmateria))
    else:
        alunos = grupoD.listar_alunos_nao_vinculados(grupo_id, idmateria)
        return render_template('vincular_aluno_grupo.html', grupo_id=grupo_id,
                               alunos=alunos, idmateria=idmateria)


@app.route('/remover_aluno_grupo/<int:grupo_id>/<int:idmateria>',
           methods=['GET', 'POST'])
@jwt_required()
@professor_required
def remover_aluno_grupo(grupo_id, idmateria):
    if request.method == 'POST':
        aluno_id = request.form['aluno']
        grupoD.remover_aluno(grupo_id, aluno_id)
        flash('Aluno removido do grupo com sucesso!', 'success')
        return redirect(url_for('grupo', materia_id=idmateria))
    else:
        alunos = grupoD.listar_alunos_vinculados(grupo_id)
        return render_template('remover_aluno_grupo.html', grupo_id=grupo_id,
                               alunos=alunos, idmateria=idmateria)


@app.route('/ver_alunos_grupo/<int:grupo_id>/<int:idmateria>', methods=['GET'])
@jwt_required()
@professor_required
def ver_alunos_grupo(grupo_id, idmateria):
    alunos_com_notas = []
    alunos = grupoD.listar_alunos_vinculados(grupo_id)
    arrendodamento = configuracoes.buscar_por_chave("Arredondamento")

    for aluno in alunos:
        idAluno = aluno[0]
        notasGeraisAluno = alunoNotasGerais.buscar_por_idAluno_materia(
            idAluno, idmateria)
        notas360Aluno = alunoAvaliacao360.buscar_por_idAluno_materia(
            idAluno, idmateria)

        nota = alunoDAO.calcula_nota(notasGeraisAluno, notas360Aluno)
        nota = arredondador.arredondar(nota, arrendodamento[2])

        aluno_com_nota = (aluno[0], aluno[1], nota)
        alunos_com_notas.append(aluno_com_nota)

    return render_template('ver_alunos_grupo.html', grupo_id=grupo_id,
                           alunos=alunos_com_notas,
                           arrendodamento=arrendodamento,
                           idmateria=idmateria)


@app.route('/criar_autoavaliacao/<int:idmateria>', methods=['GET'])
@jwt_required()
@professor_required
def criar_autoavaliacao(idmateria):
    grupos = grupoD.buscar_por_materia(idmateria)

    for grupo in grupos:
        alunos = alunoDAO.buscar_alunos_por_grupo(grupo[0])

        for aluno in alunos:
            alunoDAO.criar_autoavaliacao(completo=False, idmateria=idmateria,
                                         idaluno=aluno[0])
            user = usuarios.buscar_por_id(aluno[3])
            if user:
                Thread(target=enviar_email_assincrono,
                       args=(user, "Auto avaliação disponivel",
                             "Olá, a uma nova autoavalição para ser feita,"
                             " acesse o sistema em: <br>" +
                             "<a href = " + '"' +
                             "http://notasprofessor.tech/login" + '"' +
                             ">http://notasprofessor.tech/login</a>")).start()

    flash("Avaliações criadas com sucesso!", "success")
    return redirect(url_for('grupo', materia_id=idmateria))


@app.route('/criar_avaliacao_grupo/<int:idmateria>', methods=['GET'])
@jwt_required()
@professor_required
def criar_avaliacao_grupo(idmateria):
    grupos = grupoD.buscar_por_materia(idmateria)
    email_enviado_para = set()  # Manter um registro dos alunos para quem
    # o email já foi enviado

    for grupo in grupos:
        alunos = alunoDAO.buscar_alunos_por_grupo(grupo[0])

        for aluno_avaliado in alunos:
            for aluno_realizando in alunos:
                if aluno_avaliado[0] != aluno_realizando[0]:
                    alunoDAO.criar_avaliacao(False, idmateria,
                                             aluno_avaliado[0],
                                             aluno_realizando[0])
                    if aluno_realizando[3] not in email_enviado_para:
                        user = usuarios.buscar_por_id(aluno_realizando[3])
                        if user:
                            Thread(target=enviar_email_assincrono,
                                   args=(
                                       user, "Avaliação de Equipe disponivel",
                                       "Olá, a uma nova avaliação de"
                                       " equipe para"
                                       " ser feita, acesse o sistema em:"
                                       " <br>" +
                                       "<a href = " + '"' +
                                       "http://notasprofessor.tech/login"
                                       + '"' +
                                       ">http://notasprofessor.tech/login</a>"
                                   )).start()
                            email_enviado_para.add(aluno_realizando[3])

    flash("Avaliações criadas com sucesso!", "success")
    return redirect(url_for('grupo', materia_id=idmateria))


@app.route('/minhas_avaliacoes', methods=['GET'])
@jwt_required()
def minhas_avaliacoes():
    user_identity = get_jwt_identity()
    idusuario = user_identity["id"]
    avaliacoes = alunoDAO.buscar_avaliacoes_por_usuario_au(idusuario)

    return render_template('minhas_avaliacoes.html', avaliacoes=avaliacoes)


@app.route('/realizar_avaliacao/<int:idavaliacao>', methods=['GET', 'POST'])
@jwt_required()
def realizar_avaliacao(idavaliacao):
    avaliacao = alunoAvaliacao360.buscar_por_id_ul(idavaliacao)

    if not avaliacao:
        flash('Avaliação não encontrada ou ja realiazada', 'error')
        return redirect(url_for('minhas_avaliacoes'))

    if request.method == 'POST':
        if not alunoAvaliacao360.verificarNotaVazia(request):
            flash('Existe alguma nota em branco.', 'error')
            return redirect(
                url_for('realizar_avaliacao', idavaliacao=idavaliacao))

        if not alunoAvaliacao360.verificarNotaMaiorQueDez(request):
            flash('Existe alguma nota maior que 10.', 'error')
            return redirect(
                url_for('realizar_avaliacao', idavaliacao=idavaliacao))

        tipoAvaliacaoRealizada = 0

        if avaliacao[3] == avaliacao[4]:
            tipoAvaliacaoRealizada = 1
        else:
            tipoAvaliacaoRealizada = 3

        idAvaliacao = avaliacao360.salvar({
            'idtipo_avaliacao': tipoAvaliacaoRealizada,
            'comunicacao': float(request.form['pComunicacao']),
            'cognitivo': float(request.form['pCognitivo']),
            'autogestao': float(request.form['pAutogestao']),
            'autonomia': float(request.form['pAutonomia']),
            'protagonismo': float(request.form['pProtagonismo']),
            'interacao': float(request.form['pInteracao']),
            'idmateria': avaliacao[2]
        })

        alunoAvaliacao360.salvar({
            'idAluno': avaliacao[3],
            'idavaliacao_360': idAvaliacao,
        })

        alunoAvaliacao360.atualizar_completo(idavaliacao)

        flash('Avaliação realizada com sucesso.', 'success')
        return redirect(url_for('minhas_avaliacoes'))
    else:
        return render_template('realizar_avaliacao.html',
                               idavaliacao=idavaliacao)


@app.route('/minhas_notas', methods=['GET'])
@jwt_required()
def minhas_notas():
    user_identity = get_jwt_identity()
    user_id = user_identity["id"]
    aluno_id = alunoDAO.buscar_id_por_usuario(user_id)
    materias = materiaD.buscar_materias_por_usuario(user_id)
    notas_por_materia = []

    arredondamento = configuracoes.buscar_por_chave("Arredondamento")

    for materia_item in materias:
        idmateria = materia_item[0]
        notasGeraisAluno = alunoNotasGerais.buscar_por_idAluno_materia(
            aluno_id,
            idmateria)
        notas360Aluno = alunoAvaliacao360.buscar_por_idAluno_materia(aluno_id,
                                                                     idmateria)

        nota = alunoDAO.calcula_nota(notasGeraisAluno, notas360Aluno)
        nota_arredondada = arredondador.arredondar(nota, arredondamento[2])

        notas_por_materia.append({
            'materia': materia_item[1],
            'nota': nota_arredondada,
            'idmateria': idmateria,
        })

    return render_template('minhas_notas.html',
                           notas_por_materia=notas_por_materia)


@app.route('/ver_notas_detalhadas/<int:idmateria>', methods=['GET'])
@jwt_required()
def ver_notas_detalhadas(idmateria):
    user_identity = get_jwt_identity()
    user_id = user_identity["id"]
    aluno_id = alunoDAO.buscar_id_por_usuario(user_id)

    notasGeraisAluno = alunoNotasGerais.buscar_por_idAluno_materia(aluno_id,
                                                                   idmateria)
    notas360Aluno = alunoAvaliacao360.buscar_por_idAluno_materia(aluno_id,
                                                                 idmateria)

    return render_template('ver_notas_detalhadas.html',
                           notasGerais=notasGeraisAluno,
                           notas360=notas360Aluno)
