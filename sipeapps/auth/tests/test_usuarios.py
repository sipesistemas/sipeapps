from rest_framework import status

from sipeapps.auth.models import Perfil, Usuario, Token, PerfilPermissao
from sipeapps.auth.serializers import UsuarioSerializer
from sipeapps.common.test_base import TestBaseAtoi


class UsuarioAPITest(TestBaseAtoi):
    url_base = '/auth/usuarios/'

    def setUp(self):
        self.usuario = Usuario()
        self.usuario.login = 'user'
        self.usuario.is_admin = True
        self.usuario.set_senha(123)
        self.usuario.save()

        Token.objects.create(usuario=self.usuario, chave=123)
        self.serializer = UsuarioSerializer(instance=self.usuario)
        self.client.credentials(HTTP_AUTHORIZATION='Token 123')

        self.perfil = Perfil.objects.create(nome='Perfil')
        # self.perfil_permissao = PerfilPermissao.objects.create()

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), {'id', 'login', 'nome_completo', 'apelido', 'email', 'is_ativo', 'is_admin', 'datahora_cadastro', 'datahora_alteracao', 'perfil'})

    def test_cadastrar(self):
        self.data = {
            'login': 'hugo',
            'perfil': self.perfil.id,
            'senha': '123',
            'nome_completo': 'Hugo Henrique',
            'apelido': 'Hugo',
            'email': 'hugohomesquita@gmail.com',
            'is_ativo': True,
            'is_admin': False,
        }
        response = self.client.post(self.url_base, self.data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_nao_permitir_login_ja_utilizado(self):
        self.data = {
            'login': 'user',
            'perfil': self.perfil.id,
            'senha': '123',
            'nome_completo': 'Hugo Henrique',
            'apelido': 'Hugo',
            'email': 'hugohomesquita@gmail.com',
            'is_ativo': True,
            'is_admin': False,
        }
        response = self.client.post(self.url_base, self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response = self.decode_response(response)
        assert response['login'][0] == 'usuario com este login já existe.'

    def test_nao_permitir_senha_menor_que_3_caracteres(self):
        self.data = {
            'login': 'hugo',
            'perfil': self.perfil.id,
            'senha': '12',
            'nome_completo': 'Hugo Henrique',
            'apelido': 'Hugo',
            'email': 'hugohomesquita@gmail.com',
            'is_ativo': True,
            'is_admin': False,
        }
        response = self.client.post(self.url_base, self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response = self.decode_response(response)
        assert response['senha'][0] == 'A senha deve conter 3 ou mais caracteres.'

    def test_nao_permitir_login_invalido(self):
        new_name = {
            'login': '*'
        }
        response = self.client.patch(self.url_base + str(self.usuario.id) + "/", new_name)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response = self.decode_response(response)
        assert response['login'][0] == 'Digite um login válido. Este valor pode conter apenas letras, número e @/./+/-/_ caracteres.'

    def test_listar(self):
        response = self.client.get(self.url_base, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_atualizar(self):
        new_name = {
            'nome_completo': 'TESTE'
        }
        response = self.client.patch(self.url_base + str(self.usuario.id) + "/", new_name)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['nome_completo'] == new_name['nome_completo']

    def test_logar_apos_atualizar_usuario(self):
        # Atualizando o usuário
        new_name = {
            'nome_completo': 'TESTE'
        }
        response = self.client.patch(self.url_base + str(self.usuario.id) + "/", new_name)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['nome_completo'] == Usuario.objects.get(pk=self.usuario.id).nome_completo

        # Tentando autenticar
        response = self.client.post('/auth/token/', {'login': 'user', 'senha': 123})
        assert response.status_code == status.HTTP_200_OK
        response = self.decode_response(response)
        assert response['token']

    def test_excluir(self):
        response = self.client.delete(self.url_base + str(self.usuario.id) + "/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
