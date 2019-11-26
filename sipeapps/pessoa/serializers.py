from rest_framework import serializers

from sipeapps.pessoa.models import Cliente, Profissao


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'nome', 'apelido', 'tipo_pessoa', 'cnpj', 'cpf', 'rg', 'sexo', 'data_nascimento',
                  'profissao', 'foto_perfil', 'contatos', 'enderecos', 'tags', 'observacoes',)


class ProfissaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissao
        fields = ('id', 'nome')
