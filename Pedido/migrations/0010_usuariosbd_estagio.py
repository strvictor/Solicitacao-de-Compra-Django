# Generated by Django 5.0.4 on 2024-05-12 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedido', '0009_alter_dados_data_limite'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuariosbd',
            name='estagio',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]