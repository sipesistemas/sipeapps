import datetime
from rest_framework import status

from sipeapps.financeiro.models import Conta
from sipeapps.financeiro.serializers import ContaSerializer
from sipeapps.financeiro.tests.test_base import TestBaseAtoi


class ContasAPITest(TestBaseAtoi):
    url_base = '/financeiro/contas/'

    def setUp(self):
        self.conta = Conta.objects.create(tipo=Conta.CONTA_CORRENTE, saldo_inicial=0, data_saldo_inicial=datetime.date(2019, 11, 5))
        self.serializer = ContaSerializer(instance=self.conta)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), {'id', 'nome', 'tipo', 'saldo_inicial', 'data_saldo_inicial'})

    def test_cadastrar(self):
        self.data = {
            'nome': 'Teste2',
            'tipo': Conta.CONTA_CORRENTE,
            'data_saldo_inicial': '14/10/2010',
            'saldo_inicial': '1000.00',
        }
        response = self.client.post(self.url_base, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_listar(self):
        response = self.client.get(self.url_base, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_atualizar(self):
        new_name = {
            'nome': 'TESTE'
        }
        response = self.client.patch(self.url_base + str(self.conta.id) + "/", new_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], new_name['nome'])

    def test_excluir(self):
        response = self.client.delete(self.url_base + str(self.conta.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
