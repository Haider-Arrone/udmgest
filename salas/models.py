from django.db import models

# Create your models here.

class Sala(models.Model):
    nome = models.CharField(max_length=100)
    capacidade = models.IntegerField()

    def __str__(self):
        return self.nome

class Ocupacao(models.Model):
    
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    ESTADO_CHOICES = [
        ('Livre', 'Livre'),
        ('Ocupado', 'Ocupado'),
    ]
    estado = models.CharField(max_length=25, choices=ESTADO_CHOICES)
    
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    TURNO_CHOICES = [
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Vespertino'),
        ('Nocturno', 'Nocturno'),
    ]
    turno = models.CharField(max_length=25, choices=TURNO_CHOICES)
    FACULDADE_CHOICES = [
        ('FCJ', 'FCJ'),
        ('FCES', 'FCES'),
        ('FCT', 'FCT'),
    ]
    faculdade = models.CharField(max_length=25, choices=FACULDADE_CHOICES)
    DIAS_CHOICES = [
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]
    dia_semana = models.CharField(max_length=10, choices=DIAS_CHOICES)
    TEMPO_CHOICES = [
        (1, '1º tempo'),
        (2, '2º tempo'),
        (3, '3º tempo'),
        (4, '4º tempo'),
    ]
    tempo = models.IntegerField(choices=TEMPO_CHOICES)
    def __str__(self):
        return f"{self.sala.nome} - {self.hora_inicio} to {self.hora_fim}"
