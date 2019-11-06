from django.db import models
from rest_framework import serializers

from sipeapps.common.models import AbstratoModel


class CategoriaFinanceiro(AbstratoModel):
    RECEITA = 'RECEITA'
    DESPESA = 'DESPESA'

    NATUREZA_CHOICES = (
        (RECEITA, 'Receita'),
        (DESPESA, 'Despesa')
    )
    natureza = models.CharField(max_length=20, choices=NATUREZA_CHOICES)
    nome = models.CharField(max_length=50, unique=True)
    categoria_pai = models.ForeignKey(to='self', related_name='categorias_filhas', on_delete=models.PROTECT, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.categoria_pai and self.pk == self.categoria_pai.id:
            raise serializers.ValidationError('Uma categoria não pode ser subcategoria dela mesma.')

        if self.categoria_pai:
            # Verificar se a categoria é categoria_pai da categoria informada
            for cat in self.categorias_filhas.all():
                if cat.categoria_pai == self:
                    raise serializers.ValidationError('Não é permitido ser subcategoria desta categoria.')

        return super(CategoriaFinanceiro, self).save(*args, **kwargs)


class Conta(AbstratoModel):
    CONTA_CORRENTE = 'CONTA_CORRENTE'
    CARTAO = 'CARTAO'
    CLIENTE = 'CLIENTE'
    TIPO_CHOICES = (
        (CONTA_CORRENTE, 'Conta corrente'),
        (CARTAO, 'Cartão'),
        (CLIENTE, 'Cliente')
    )
    nome = models.CharField(max_length=255, unique=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    saldo_inicial = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    data_saldo_inicial = models.DateField()
