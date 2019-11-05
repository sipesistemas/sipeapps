from rest_framework import status
from rest_framework.test import APITestCase


class ContaAPITest(APITestCase):
    url_base = "/financeiro/contas/"

    def setUp(self):
        pass

    def test_contains_expected_fields(self):
        self.assertEqual(True, True)

    def test_ler(self):
        response = self.client.get(self.url_base, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
