from django.db import models


class AbstratoModel(models.Model):
    datahora_cadastro = models.DateTimeField(auto_now_add=True)
    datahora_alteracao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
