from django.db import models
from expedient.models import Funcionario
from django.contrib.auth.models import User

class Autorizacao(models.Model):
    AVALIACAO_CHOICES = [
        ('teste_1', '1º Teste'),
        ('teste_2', '2º Teste'),
        ('exame', 'Exame'),
        ('exame_recorrencia', 'Exame de Recorrência'),
    ]
    estudante_nome = models.CharField(max_length=100) 
    disciplina = models.CharField(max_length=100, null=True, blank=True) 
    avaliacao_nome = models.CharField(max_length=100, choices=AVALIACAO_CHOICES)
    data_avaliacao = models.DateField()
    autorizado = models.BooleanField(default=True, null=True, blank=True)
    justificativa = models.TextField(null=True, blank=True)  # Justificativa da autorização ou não
    data_autorizacao = models.DateTimeField(auto_now_add=True)
    responsavel = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)
    
    
    def __str__(self):
        return f"Autorização para {self.estudante_nome} "