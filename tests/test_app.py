
def test_lista_alunos(client):
    response = client.get('/')
    assert response.status_code == 200


def test_adicionar_aluno(client):
    response = client.get('/adicionar_aluno')
    assert response.status_code == 200


def test_deletar_aluno(client):
    response = client.get('/deletar_aluno/1')
    assert response.status_code == 200


def test_editar_aluno(client):
    response = client.get('/editar_aluno/1')
    assert response.status_code == 200


def test_adicionar_nota(client):
    response = client.get('/adicionar_nota/1/1/1')
    assert response.status_code == 200


def test_adicionar_nota_360(client):
    response = client.get('/adicionar_nota_360/1/1/1')
    assert response.status_code == 200


def test_detalhes(client):
    response = client.get('/detalhes/1/1/1')
    assert response.status_code == 200


def test_deletar_gerais(client):
    response = client.get('/deletar_gerais/1/1/1')
    assert response.status_code == 200


def test_editar_gerais(client):
    response = client.get('/editar_gerais/1/1/1')
    assert response.status_code == 200


def test_deletar_360(client):
    response = client.get('/deletar_360/1/1/1')
    assert response.status_code == 200


def test_editar_360(client):
    response = client.get('/editar_360/1/1/1')
    assert response.status_code == 200


def test_alterar_arredondamento(client):
    response = client.post('/alterar_arredondamento/1/1')
    assert response.status_code == 200


def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200


def test_registro_usuario(client):
    response = client.get('/registro_usuario')
    assert response.status_code == 200


def test_verificar_codigo(client):
    response = client.get('/verificar_codigo')
    assert response.status_code == 200


def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 200


def test_home(client):
    response = client.get('/home')
    assert response.status_code == 200


def test_dashboard(client):
    response = client.get('/dashboard')
    assert response.status_code == 200


def test_esqueci_senha(client):
    response = client.get('/esqueci_senha')
    assert response.status_code == 200


def test_mudar_senha(client):
    response = client.get('/mudar_senha')
    assert response.status_code == 200


def test_lista_usuario(client):
    response = client.get('/lista_usuario')
    assert response.status_code == 200


def test_aprovar_usuario(client):
    response = client.get('/aprovar_usuario/1')
    assert response.status_code == 200


def test_excluir_usuario(client):
    response = client.get('/excluir_usuario/1')
    assert response.status_code == 200


def test_editar_usuario(client):
    response = client.get('/editar_usuario/1')
    assert response.status_code == 200


def test_materia(client):
    response = client.get('/materia')
    assert response.status_code == 200


def test_turma(client):
    response = client.get('/turma')
    assert response.status_code == 200


def test_grupo(client):
    response = client.get('/grupo/1')
    assert response.status_code == 200


def test_adicionar_materia(client):
    response = client.get('/adicionar_materia')
    assert response.status_code == 200


def test_adicionar_turma(client):
    response = client.get('/adicionar_turma')
    assert response.status_code == 200


def test_adicionar_grupo(client):
    response = client.get('/adicionar_grupo/1')
    assert response.status_code == 200


def test_editar_materia(client):
    response = client.get('/editar_materia/1')
    assert response.status_code == 200


def test_editar_turma(client):
    response = client.get('/editar_turma/1')
    assert response.status_code == 200


def test_editar_grupo(client):
    response = client.get('/editar_grupo/1')
    assert response.status_code == 200


def test_deletar_materia(client):
    response = client.get('/deletar_materia/1')
    assert response.status_code == 200


def test_deletar_turma(client):
    response = client.get('/deletar_turma/1')
    assert response.status_code == 200


def test_deletar_grupo(client):
    response = client.get('/deletar_grupo/1')
    assert response.status_code == 200


def test_vincular_aluno(client):
    response = client.get('/turma/1/vincular_aluno')
    assert response.status_code == 200


def test_remover_aluno(client):
    response = client.get('/turma/1/remover_aluno')
    assert response.status_code == 200


def test_ver_alunos(client):
    response = client.get('/turma/1/ver_alunos')
    assert response.status_code == 200


def test_vincular_aluno_grupo(client):
    response = client.get('/vincular_aluno_grupo/1/1')
    assert response.status_code == 200


def test_remover_aluno_grupo(client):
    response = client.get('/remover_aluno_grupo/1/1')
    assert response.status_code == 200


def test_ver_alunos_grupo(client):
    response = client.get('/ver_alunos_grupo/1/1')
    assert response.status_code == 200


def test_criar_autoavaliacao(client):
    response = client.get('/criar_autoavaliacao/1')
    assert response.status_code == 200


def test_criar_avaliacao_grupo(client):
    response = client.get('/criar_avaliacao_grupo/1')
    assert response.status_code == 200


def test_minhas_avaliacoes(client):
    response = client.get('/minhas_avaliacoes')
    assert response.status_code == 200


def test_realizar_avaliacao(client):
    response = client.get('/realizar_avaliacao/1')
    assert response.status_code == 200


def test_minhas_notas(client):
    response = client.get('/minhas_notas')
    assert response.status_code == 200


def test_ver_notas_detalhadas(client):
    response = client.get('/ver_notas_detalhadas/1')
    assert response.status_code == 200


def test_gerenciar_alunos(client):
    response = client.get('/gerenciar_alunos')
    assert response.status_code == 200


def test_vincular_usuario(client):
    response = client.get('/vincular_usuario/1')
    assert response.status_code == 200


def test_desvincular_usuario(client):
    response = client.get('/desvincular_usuario/1')
    assert response.status_code == 200
