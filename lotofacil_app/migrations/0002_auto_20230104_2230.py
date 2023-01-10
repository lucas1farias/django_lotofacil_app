# Generated by Django 3.2.13 on 2023-01-05 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lotofacil_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Última atualização')),
                ('availability', models.BooleanField(default=True, verbose_name='Disponibilidade')),
                ('game_text', models.CharField(max_length=100, verbose_name='Digite cada número do jogo separado por barra de espaço (ex: 1 2 4 6 7 8 10 11 14 15 16 17 20 21 24)')),
            ],
            options={
                'verbose_name': 'Aniversário',
                'verbose_name_plural': 'Aniversários',
            },
        ),
        migrations.DeleteModel(
            name='SignIdentifierAlgorithmModel',
        ),
    ]
