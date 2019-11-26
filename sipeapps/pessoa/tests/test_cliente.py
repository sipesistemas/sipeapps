from rest_framework import status

from sipeapps.pessoa.models import Cliente
from sipeapps.pessoa.serializers import ClienteSerializer
from sipeapps.common.test_base import TestBaseAtoi


class ClientesAPITest(TestBaseAtoi):
    url_base = '/pessoa/clientes/'
    fixtures = ['usuario']

    def setUp(self):
        self.cliente = Cliente.objects.create(nome="Hugo Mesquita")
        self.serializer = ClienteSerializer(instance=self.cliente)
        self.client.credentials(HTTP_AUTHORIZATION='Token 123')

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), {'id', 'nome', 'apelido', 'tipo_pessoa', 'cnpj', 'cpf', 'rg', 'sexo', 'data_nascimento',
                                            'profissao', 'foto_perfil', 'contatos', 'enderecos', 'tags', 'observacoes'})

    def test_cadastrar_simples(self):
        self.data = {
            'nome': "Hugo Henrique",
            'apelido': 'Hugo',
        }
        response = self.client.post(self.url_base, self.data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_cadastrar_cliente_pf(self):
        self.data = {
            'nome': "Hugo Henrique",
            'apelido': 'Hugo',
            'tipo_pessoa': Cliente.FISICA
        }
        response = self.client.post(self.url_base, self.data)
        assert response.status_code == status.HTTP_201_CREATED
        response = self.decode_response(response)
        assert response['nome'] == self.data['nome']
        assert response['apelido'] == self.data['apelido']
        assert response['tipo_pessoa'] == self.data['tipo_pessoa']

    def test_nao_cadastrar_cliente_pf_com_cpf_ja_existente(self):
        self.data = {
            'nome': "Hugo Henrique",
            'apelido': 'Hugo',
            'tipo_pessoa': Cliente.FISICA,
            'cpf': '072.277.624-16'
        }
        response = self.client.post(self.url_base, self.data)
        assert response.status_code == status.HTTP_201_CREATED
        self.data = {
            'nome': "Hugo Henrique",
            'apelido': 'Hugo',
            'tipo_pessoa': Cliente.FISICA,
            'cpf': '072.277.624-16'
        }
        response = self.client.post(self.url_base, self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response = self.decode_response(response)
        assert response['cpf'][0] == 'Já existe um cliente cadastrado com este CPF.'

    def test_nao_cadastrar_cliente_pj_com_cnpj_ja_existente(self):
        self.data = {
            'nome': "Sipe Sistemas",
            'apelido': 'SIPE',
            'tipo_pessoa': Cliente.JURIDICA,
            'cnpj': '28.378.899/0001-08'
        }
        response = self.client.post(self.url_base, self.data)
        assert response.status_code == status.HTTP_201_CREATED
        self.data = {
            'nome': "Sipe Sistemas",
            'apelido': 'SIPE',
            'tipo_pessoa': Cliente.JURIDICA,
            'cnpj': '28.378.899/0001-08'
        }
        response = self.client.post(self.url_base, self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response = self.decode_response(response)
        assert response['cnpj'][0] == 'Já existe um cliente cadastrado com este CNPJ.'

    def test_listar(self):
        response = self.client.get(self.url_base, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_atualizar(self):
        new_name = {
            'nome': 'TESTE'
        }
        response = self.client.patch(self.url_base + str(self.cliente.id) + "/", new_name)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['nome'] == new_name['nome']

    def test_nao_atualizar_cliente_pf_com_cpf_ja_existente(self):
        self.cliente.tipo_pessoa = Cliente.FISICA
        self.cliente.cpf = '072.277.624-16'
        self.cliente.save()
        self.new_cliente = Cliente()
        self.new_cliente.nome = "Teste"
        self.new_cliente.tipo_pessoa = Cliente.FISICA
        self.new_cliente.cpf = '474.597.354-34'
        self.new_cliente.save()
        new_name = {
            'cpf': '072.277.624-16'
        }
        response = self.client.patch(self.url_base + str(self.new_cliente.id) + "/", new_name)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response = self.decode_response(response)
        assert response['cpf'][0] == 'Já existe um cliente cadastrado com este CPF.'

    def test_nao_atualizar_cliente_pj_com_cnpj_ja_existente(self):
        self.cliente.tipo_pessoa = Cliente.JURIDICA
        self.cliente.cnpj = '28.378.899/0001-08'
        self.cliente.save()
        self.new_cliente = Cliente()
        self.new_cliente.nome = "Teste"
        self.new_cliente.tipo_pessoa = Cliente.JURIDICA
        self.new_cliente.cnpj = '11.111.111/0001-00'
        self.new_cliente.save()
        new_name = {
            'cnpj': '28.378.899/0001-08'
        }
        response = self.client.patch(self.url_base + str(self.new_cliente.id) + "/", new_name)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response = self.decode_response(response)
        assert response['cnpj'][0] == 'Já existe um cliente cadastrado com este CNPJ.'

    def test_atualizar_cliente_cpf(self):
        self.cliente.tipo_pessoa = Cliente.FISICA
        self.cliente.cpf = '072.277.624-16'
        self.cliente.save()
        self.new_cliente = Cliente()
        self.new_cliente.nome = "Teste"
        self.new_cliente.tipo_pessoa = Cliente.FISICA
        self.new_cliente.cpf = '474.597.354-34'
        self.new_cliente.save()
        new_name = {
            'cpf': '072.277.624-16'
        }
        response = self.client.patch(self.url_base + str(self.cliente.id) + "/", new_name)
        assert response.status_code == status.HTTP_200_OK

    def test_atualizar_cliente_cnpj(self):
        self.cliente.tipo_pessoa = Cliente.JURIDICA
        self.cliente.cnpj = '28.378.899/0001-08'
        self.cliente.save()
        self.new_cliente = Cliente()
        self.new_cliente.nome = "Teste"
        self.new_cliente.tipo_pessoa = Cliente.JURIDICA
        self.new_cliente.cnpj = '11.111.111/0001-00'
        self.new_cliente.save()
        new_name = {
            'cnpj': '28.378.899/0001-08'
        }
        response = self.client.patch(self.url_base + str(self.cliente.id) + "/", new_name)
        assert response.status_code == status.HTTP_200_OK

    def test_excluir(self):
        response = self.client.delete(self.url_base + str(self.cliente.id) + "/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
