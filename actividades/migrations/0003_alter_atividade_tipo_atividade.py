# Generated by Django 4.0.6 on 2024-10-28 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0002_alter_atividade_funcionario_tipoatividade_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atividade',
            name='tipo_atividade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='atividades_tipo', to='actividades.tipoatividade'),
        ),
    ]