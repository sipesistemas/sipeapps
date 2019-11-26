# Generated by Django 2.2.7 on 2019-11-26 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datahora_cadastro', models.DateTimeField(auto_now_add=True)),
                ('datahora_alteracao', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=255, unique=True)),
                ('tipo', models.CharField(choices=[('CONTA_CORRENTE', 'Conta corrente'), ('CARTAO', 'Cartão'), ('CLIENTE', 'Cliente')], max_length=50)),
                ('saldo_inicial', models.DecimalField(decimal_places=3, default=0, max_digits=15)),
                ('data_saldo_inicial', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datahora_cadastro', models.DateTimeField(auto_now_add=True)),
                ('datahora_alteracao', models.DateTimeField(auto_now=True)),
                ('natureza', models.CharField(choices=[('RECEITA', 'Receita'), ('DESPESA', 'Despesa')], max_length=20)),
                ('nome', models.CharField(max_length=50, unique=True)),
                ('categoria_pai', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='categorias_filhas', to='financeiro.Categoria')),
            ],
            options={
                'db_table': 'financeiro_categoria',
            },
        ),
    ]
