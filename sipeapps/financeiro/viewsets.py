from rest_framework import viewsets

from sipeapps.financeiro.models import Conta
from sipeapps.financeiro.serializers import ContaSerializer


class ContaViewset(viewsets.ModelViewSet):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
