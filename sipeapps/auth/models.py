import binascii
import hashlib
import os

from django.db import models
from rest_framework import serializers

from sipeapps.auth.validators import UnicodeLoginValidator
from sipeapps.common.models import AbstratoModel


class Usuario(AbstratoModel):
    login = models.CharField(max_length=150, unique=True, validators=[UnicodeLoginValidator()])
    senha = models.CharField(max_length=150)
    nome_completo = models.CharField(max_length=50, blank=True)
    apelido = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    perfil = models.ForeignKey(to='Perfil', related_name='perfil', blank=True, null=True, on_delete=models.PROTECT)
    foto_perfil = models.ImageField(blank=True, null=True)

    is_ativo = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def save(self, *args, **kwargs):
        self.nome_completo = self.nome_completo.strip()
        self.apelido = self.apelido.strip()

        if not self.perfil and not self.is_admin:
            raise serializers.ValidationError({'perfil': ['Necessário informar o perfil.']})

        super(Usuario, self).save(*args, **kwargs)

    def set_senha(self, senha):
        if len(str(senha)) < 3:
            raise serializers.ValidationError({'senha': ['A senha deve conter 3 ou mais caracteres.']})
        senha_md5 = hashlib.md5(str(senha).encode()).hexdigest()
        self.senha = senha_md5


class Token(AbstratoModel):
    usuario = models.ForeignKey(to='Usuario', related_name='tokens', on_delete=models.CASCADE)
    chave = models.CharField(max_length=40, primary_key=True)

    def save(self, *args, **kwargs):
        if not self.chave:
            self.chave = self.gerar_chave()
        return super().save(*args, **kwargs)

    def gerar_chave(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.chave


class Perfil(AbstratoModel):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'auth_perfil'
        ordering = ('nome',)


class PerfilPermissao(AbstratoModel):
    perfil = models.ForeignKey(to='Perfil', related_name='permissoes', on_delete=models.CASCADE)
    codigo = models.CharField(max_length=200)

    class Meta:
        db_table = 'auth_perfil_permissao'
        unique_together = ('perfil', 'codigo')

    def save(self, *args, **kwargs):
        self.codigo = str(self.codigo).lower()
        super(PerfilPermissao, self).save(*args, **kwargs)
