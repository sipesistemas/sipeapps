from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from sipeapps.financeiro.models import Conta, Categoria
from sipeapps.financeiro.serializers import ContaSerializer, CategoriaFinanceiroSerializer, CategoriaFinanceiroTreeSerializer


class CategoriaFinanceiroViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaFinanceiroSerializer

    @action(methods=['GET'], detail=False)
    def tree(self, request):
        queryset = Categoria.objects.filter(categoria_pai=None).order_by('-nome')
        serializer = CategoriaFinanceiroTreeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContaViewset(viewsets.ModelViewSet):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
    public_permissions = ['tree']

    @action(methods=['GET'], detail=False)
    def tree(self, request):
        return Response('')
