from rest_framework import serializers

from sipeapps.financeiro.models import Conta, CategoriaFinanceiro


class CategoriaFinanceiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaFinanceiro
        fields = ('id', 'nome', 'categoria_pai', 'natureza')


class CategoriaFinanceiroTreeSerializer(serializers.ModelSerializer):
    class _RecursiveSerializer(serializers.Serializer):
        def to_representation(self, value):
            serializer = self.parent.parent.__class__(value, context=self.context)
            return serializer.data

    categorias_filhas = _RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = CategoriaFinanceiro
        fields = ('id', 'nome', 'categoria_pai', 'categorias_filhas', 'natureza')


class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ('id', 'nome', 'saldo_inicial', 'tipo', 'data_saldo_inicial')
