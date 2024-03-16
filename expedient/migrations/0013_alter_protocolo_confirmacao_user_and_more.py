# Generated by Django 4.0.6 on 2024-01-03 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expedient', '0012_protocolo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protocolo',
            name='confirmacao_user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='confirmacao_user', to='expedient.funcionario'),
        ),
        migrations.AlterField(
            model_name='protocolo',
            name='data_confirmacao_recepcao',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='protocolo',
            name='remetente',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='remetente', to='expedient.funcionario'),
        ),
    ]