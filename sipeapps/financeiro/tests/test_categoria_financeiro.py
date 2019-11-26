from rest_framework import status
from rest_framework.exceptions import ValidationError

from sipeapps.common.test_base import TestBaseAtoi
from sipeapps.financeiro.models import Categoria
from sipeapps.financeiro.serializers import CategoriaFinanceiroSerializer


class CategoriaFinanceiroTest(TestBaseAtoi):
    url_base = "/financeiro/categorias/"
    fixtures = ['usuario']

    def setUp(self):
        self.categoria = Categoria.objects.create(nome='CAT A', natureza=Categoria.RECEITA)
        self.serializer = CategoriaFinanceiroSerializer(instance=self.categoria)
        self.client.credentials(HTTP_AUTHORIZATION='Token 123')

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), {'id', 'nome', 'categoria_pai', 'natureza'})

    def test_cadastrar(self):
        self.data = {
            'nome': 'CAT B',
            'natureza': Categoria.RECEITA
        }
        response = self.client.post(self.url_base, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cadastrar_subcategoria(self):
        self.data = {
            'nome': 'CAT A1',
            'categoria_pai': self.categoria.pk,
            'natureza': Categoria.RECEITA
        }
        response = self.client.post(self.url_base, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.categoria.categorias_filhas.count(), 1)

    def test_listar(self):
        response = self.client.get(self.url_base, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_atualizar(self):
        new_name = {
            'nome': 'CAT C',
            'natureza': Categoria.RECEITA
        }
        response = self.client.patch(self.url_base + str(self.categoria.id) + "/", new_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], new_name['nome'])

    def test_excluir(self):
        response = self.client.delete(self.url_base + str(self.categoria.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_nao_permitir_a_categoria_pai_de_uma_categoria_ser_ela_mesma(self):
        # Categoria A ser filha de Categoria A
        with self.assertRaises(ValidationError) as c:
            cat_a = Categoria.objects.create(nome="Categoria A")
            cat_a.categoria_pai = cat_a
            cat_a.save()
        self.assertEqual(c.exception.detail[0], 'Uma categoria não pode ser subcategoria dela mesma.')

    def test_nao_permitir_a_ciclo_entre_as_categorias(self):
        # CAT B ser filha de CAT A
        # CAT A ser filha de CAT B
        cat_a = Categoria.objects.create(nome="Categoria A")
        cat_b = Categoria.objects.create(nome="Categoria B")

        cat_b.categoria_pai = cat_a
        cat_b.save()
        with self.assertRaises(ValidationError) as c:
            cat_a.categoria_pai = cat_b
            cat_a.save()
        self.assertEqual(c.exception.detail[0], 'Não é permitido ser subcategoria desta categoria.')

    def test_retornar_tree_das_categorias(self):
        Categoria.objects.all().delete()
        cat_a = Categoria.objects.create(nome="Categoria A", natureza=Categoria.RECEITA)
        cat_b = Categoria.objects.create(nome="Categoria B", categoria_pai=cat_a, natureza=Categoria.RECEITA)
        cat_c = Categoria.objects.create(nome="Categoria C", categoria_pai=cat_b, natureza=Categoria.RECEITA)

        cat_d = Categoria.objects.create(nome="Categoria D", natureza=Categoria.DESPESA)
        cat_e = Categoria.objects.create(nome="Categoria E", categoria_pai=cat_d, natureza=Categoria.DESPESA)
        cat_f = Categoria.objects.create(nome="Categoria F", categoria_pai=cat_d, natureza=Categoria.DESPESA)

        response = self.client.get(self.url_base + "tree/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = self.decode_response(response)

        # PRIMEIRO CASO
        self.assertEqual(data[0]['id'], cat_d.id)
        self.assertEqual(data[0]['categoria_pai'], None)
        self.assertEqual(len(data[0]['categorias_filhas']), 2)

        self.assertEqual(data[0]['categorias_filhas'][0]['id'], cat_e.id)
        self.assertEqual(data[0]['categorias_filhas'][0]['categoria_pai'], cat_d.id)
        self.assertEqual(len(data[0]['categorias_filhas'][0]['categorias_filhas']), 0)

        self.assertEqual(data[0]['categorias_filhas'][1]['id'], cat_f.id)
        self.assertEqual(data[0]['categorias_filhas'][1]['categoria_pai'], cat_d.id)
        self.assertEqual(len(data[0]['categorias_filhas'][1]['categorias_filhas']), 0)

        # SEGUNDO CASO, DA CAT D PARA BAIXO
        self.assertEqual(data[1]['id'], cat_a.id)
        self.assertEqual(data[1]['categoria_pai'], None)
        self.assertEqual(len(data[1]['categorias_filhas']), 1)

        self.assertEqual(data[1]['categorias_filhas'][0]['id'], cat_b.id)
        self.assertEqual(data[1]['categorias_filhas'][0]['categoria_pai'], cat_a.id)
        self.assertEqual(len(data[1]['categorias_filhas'][0]['categorias_filhas']), 1)

        self.assertEqual(data[1]['categorias_filhas'][0]['categorias_filhas'][0]['id'], cat_c.id)
        self.assertEqual(data[1]['categorias_filhas'][0]['categorias_filhas'][0]['categoria_pai'], cat_b.id)
        self.assertEqual(len(data[1]['categorias_filhas'][0]['categorias_filhas'][0]['categorias_filhas']), 0)
