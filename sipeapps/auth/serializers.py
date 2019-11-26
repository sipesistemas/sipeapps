import hashlib
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from sipeapps.auth.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'login', 'senha', 'nome_completo', 'apelido', 'email', 'is_ativo', 'is_admin', 'datahora_cadastro', 'datahora_alteracao', 'perfil')
        extra_kwargs = {'senha': {'write_only': True}}

    def create(self, validated_data):
        user = Usuario.objects.create(**validated_data)
        user.set_senha(validated_data['senha'])
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    login = serializers.CharField()
    senha = serializers.CharField(trim_whitespace=False)

    def validate(self, attrs):
        login = attrs.get('login')
        senha = attrs.get('senha')

        if login and senha:
            try:
                senha_md5 = hashlib.md5(senha.encode()).hexdigest()
                usuario = Usuario.objects.get(login=login, senha=senha_md5)

                if not usuario.is_ativo:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg, code='authorization')

                attrs['usuario'] = usuario
            except Usuario.DoesNotExist:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        return attrs
