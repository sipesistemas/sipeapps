from rest_framework import serializers

from sipeapps.financeiro.models import Conta


class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ('id', 'nome',)
