# Generated by Django 5.1.3 on 2025-03-22 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pautas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpauta',
            name='avaliacao',
            field=models.CharField(blank=True, choices=[('1', '1º teste'), ('2', '2º teste'), ('3', '3º teste'), ('exame', 'Exame'), ('exame_recorrencia', 'Exame de Recorrência')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pauta',
            name='avaliacao',
            field=models.CharField(blank=True, choices=[('1', '1º teste'), ('2', '2º teste'), ('3', '3º teste'), ('exame', 'Exame'), ('exame_recorrencia', 'Exame de Recorrência')], max_length=20, null=True),
        ),
    ]
