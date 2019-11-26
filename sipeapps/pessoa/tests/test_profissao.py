from rest_framework import status

from sipeapps.pessoa.models import Profissao
from sipeapps.pessoa.serializers import ProfissaoSerializer
from sipeapps.common.test_base import TestBaseAtoi


class ProfissaoAPITest(TestBaseAtoi):
    url_base = '/pessoa/profissoes/'
    fixtures = ['usuario']

    def setUp(self):
        self.profissao = Profissao.objects.create(nome='Profissao')
        self.serializer = ProfissaoSerializer(instance=self.profissao)
        self.client.credentials(HTTP_AUTHORIZATION='Token 123')

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), {'id', 'nome'})

    def test_cadastrar(self):
        self.data = {
            'nome': 'Programador',
        }
        response = self.client.post(self.url_base, self.data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_listar(self):
        response = self.client.get(self.url_base, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_atualizar(self):
        new_name = {
            'nome': 'Programador Teste'
        }
        response = self.client.patch(self.url_base + str(self.profissao.id) + "/", new_name)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['nome'] == new_name['nome']

    def test_excluir(self):
        response = self.client.delete(self.url_base + str(self.profissao.id) + "/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
