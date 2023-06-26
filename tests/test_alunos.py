import unittest

from app import app


class FlaskRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def tearDown(self):
        pass  # inserir processo de finalização

    def test_adicionar_aluno(self):
        response = self.client.post(
                                    '/adicionar_aluno',
                                    data=dict(nome='Teste'))
        self.assertEqual(response.status_code, 200)

    def test_deletar_aluno(self):
        response = self.client.get('/deletar_aluno/1')
        self.assertEqual(response.status_code, 200)

    def test_editar_aluno(self):
        response = self.client.get('/editar_aluno/1')
        self.assertEqual(response.status_code, 200)

    def test_gerenciar_alunos(self):
        response = self.client.get('/gerenciar_alunos')
        self.assertEqual(response.status_code, 200)

    def test_vincular_usuario(self):
        response = self.client.post(
                                    '/vincular_usuario/1',
                                    data=dict(idusuario='1')
                                    )
        self.assertEqual(response.status_code, 200)

    def test_desvincular_usuario(self):
        response = self.client.get('/desvincular_usuario/1')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
