from rest_framework import status

from sipeapps.auth.models import Usuario, Token
from sipeapps.auth.serializers import UsuarioSerializer
from sipeapps.common.test_base import TestBaseAtoi


class AuthLoginAPITest(TestBaseAtoi):
    url_base = '/auth/token/'

    def setUp(self):
        self.usuario = Usuario()
        self.usuario.login = 'user'
        self.usuario.is_admin = True
        self.usuario.set_senha(123)
        self.usuario.save()
        self.serializer = UsuarioSerializer(instance=self.usuario)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), {'id', 'login', 'nome_completo', 'apelido', 'email', 'is_ativo', 'is_admin', 'datahora_cadastro', 'datahora_alteracao', 'perfil'})

    def test_criacao_do_token_caso_nao_exista(self):
        assert Token.objects.count() == 0
        self.client.post(self.url_base, {'login': 'user', 'senha': 123})
        assert Token.objects.count() == 1

    def test_nao_duplicar_o_token_caso_ja_exista(self):
        assert Token.objects.count() == 0
        self.client.post(self.url_base, {'login': 'user', 'senha': 123})
        assert Token.objects.count() == 1
        self.client.post(self.url_base, {'login': 'user', 'senha': 123})
        assert Token.objects.count() == 1

    def test_login(self):
        assert Token.objects.count() == 0
        response = self.client.post(self.url_base, {'login': 'user', 'senha': 123})
        assert response.status_code == status.HTTP_200_OK
        response = self.decode_response(response)
        assert response['token']
        self.assertCountEqual(response['usuario'].keys(), {'id', 'login', 'nome_completo', 'apelido', 'email', 'is_ativo', 'is_admin', 'datahora_cadastro', 'datahora_alteracao', 'perfil'})

    def test_senha_incorreta(self):
        response = self.client.post(self.url_base, {'login': 'user', 'senha': 1234})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response = self.decode_response(response)
        assert response['non_field_errors'][0] == 'Impossível fazer login com as credenciais fornecidas.'

    def test_usuario_inativo(self):
        self.usuario.is_ativo = False
        self.usuario.save()
        response = self.client.post(self.url_base, {'login': 'user', 'senha': 123})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response = self.decode_response(response)
        assert response['non_field_errors'][0] == 'Conta de usuário desabilitada.'
