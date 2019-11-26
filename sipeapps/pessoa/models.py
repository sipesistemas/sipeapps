from django.contrib.postgres.fields import JSONField
from django.db import models
from rest_framework import serializers

from sipeapps.common.models import AbstratoModel


class Cliente(AbstratoModel):
    FISICA = 'FISICA'
    JURIDICA = 'JURIDICA'
    NAO_INFORMADO = 'NAO_INFORMADO'
    TIPO_PESSOA_CHOICES = (
        (FISICA, 'Física'),
        (JURIDICA, 'Jurídica'),
        (NAO_INFORMADO, 'Não informado'),
    )
    nome = models.CharField(max_length=255)  # Razão social
    apelido = models.CharField(max_length=50, blank=True, null=True)  # Nome Fantasia
    tipo_pessoa = models.CharField(max_length=13, choices=TIPO_PESSOA_CHOICES, default=NAO_INFORMADO)

    # Pessoa Jurídica
    cnpj = models.CharField(max_length=18, blank=True, null=True)

    # Pessoa Física
    MASCULINO = 'MASCULINO'
    FEMININO = 'FEMININO'
    SEXO_CHOICES = (
        (MASCULINO, 'Masculino'),
        (FEMININO, 'Feminino'),
    )
    cpf = models.CharField(max_length=14, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True, unique=True)
    sexo = models.CharField(max_length=255, blank=True, null=True, choices=SEXO_CHOICES)
    data_nascimento = models.DateField(blank=True, null=True)
    profissao = models.ForeignKey(to='Profissao', related_name='clientes', blank=True, null=True, on_delete=models.PROTECT)

    # Comum
    foto_perfil = models.ImageField(blank=True, null=True)
    contatos = JSONField(blank=True, null=True)
    enderecos = JSONField(blank=True, null=True)
    tags = JSONField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('nome',)

    def save(self, *args, **kwargs):
        self.cnpj = None if self.cnpj == '' else self.cnpj
        self.cpf = None if self.cpf == '' else self.cpf
        self.rg = None if self.rg == '' else self.rg

        # Não permitir cliente com o mesmo cpf ou cnpj caso seja informado
        if self.tipo_pessoa == Cliente.JURIDICA and self.cnpj:
            if Cliente.objects.filter(cnpj=self.cnpj).exclude(pk=self.id).exists():
                raise serializers.ValidationError({'cnpj': ['Já existe um cliente cadastrado com este CNPJ.']})

        if self.tipo_pessoa == Cliente.FISICA and self.cpf:
            if Cliente.objects.filter(cpf=self.cpf).exclude(pk=self.id).exists():
                raise serializers.ValidationError({'cpf': ['Já existe um cliente cadastrado com este CPF.']})

        super(Cliente, self).save(*args, **kwargs)


class Profissao(AbstratoModel):
    nome = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ('nome',)
