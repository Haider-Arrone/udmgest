# Generated by Django 4.0.6 on 2022-08-06 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=95)),
                ('numero_telefone', models.CharField(max_length=65)),
                ('estudante_interno', models.BooleanField(default=True)),
                ('instituicao', models.CharField(max_length=100)),
                ('codigo_estudante', models.IntegerField()),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
