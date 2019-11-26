import json
from rest_framework.test import APITestCase


class TestBaseAtoi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # call_command('loaddata', 'loaddata/inicial', verbosity=0)
        pass

    def decode_response(self, response):
        return json.loads(response.content.decode('utf8'))
