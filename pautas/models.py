from django.db import models
from django.contrib.auth import get_user_model
from simple_history.models import HistoricalRecords

User = get_user_model()

class Faculdade(models.Model):
    nome = models.CharField(max_length=150, unique=True, null=True, blank=True)
    
    def __str__(self):
        return self.nome

class Curso(models.Model):
    nome = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.nome

class Semestre(models.Model):
    OPCOES_SEMESTRE = [
        (1, '1º Semestre'),
        (2, '2º Semestre')
    ]
    ano = models.PositiveIntegerField(null=True, blank=True)
    semestre = models.IntegerField(choices=OPCOES_SEMESTRE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.ano} - {dict(self.OPCOES_SEMESTRE)[self.semestre]}" if self.ano and self.semestre else "Semestre Incompleto"

class Disciplina(models.Model):
    nome = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.nome

class Pauta(models.Model):
    AVALIACAO_CHOICES = [
        ('1', '1º teste'),
        ('2', '2º teste'),
        ('3', '3º teste'),
        ('exame', 'Exame'),
        ('exame_recorrencia', 'Exame de Recorrência'),
    ]
    faculdade = models.ForeignKey(Faculdade, on_delete=models.CASCADE, null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True, blank=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, null=True, blank=True)
    turma = models.CharField(max_length=50, null=True, blank=True)
    
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, null=True, blank=True)
    arquivo = models.FileField(upload_to='pautas/uploads/%Y/%m/%d/', null=True, blank=True)
    avaliacao = models.CharField(max_length=20, choices=AVALIACAO_CHOICES, null=True, blank=True)
    docente = models.CharField(max_length=50, null=True, blank=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pautas_criadas')
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pautas_modificadas')
    data_criacao = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    data_modificacao = models.DateTimeField(auto_now=True, null=True, blank=True)
    ativo = models.BooleanField(default=True, null=True, blank=True)  # Soft delete
    history = HistoricalRecords()

    def __str__(self):
        return f"Pauta - {self.disciplina.nome} ({self.turma}, {self.semestre})" if self.disciplina and self.turma and self.semestre else "Pauta Incompleta"