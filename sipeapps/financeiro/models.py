from django.db import models


class Conta(models.Model):
    nome = models.CharField(max_length=100)
