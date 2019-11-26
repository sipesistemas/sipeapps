from rest_framework import viewsets

from sipeapps.pessoa.models import Cliente, Profissao
from sipeapps.pessoa.serializers import ClienteSerializer, ProfissaoSerializer


class ClienteViewset(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ProfissaoViewset(viewsets.ModelViewSet):
    queryset = Profissao.objects.all()
    serializer_class = ProfissaoSerializer
