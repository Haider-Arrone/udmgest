# Generated by Django 4.0.6 on 2022-10-11 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expedient', '0007_parecer_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parecer',
            name='id_receptor',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='expedient.funcionario'),
        ),
    ]
