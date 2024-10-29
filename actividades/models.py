from django.db import models

from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from expedient.models import Funcionario, Departamento
# Create your models here.

class TipoAtividade(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="tipos_atividades")

    def __str__(self):
        return f"{self.nome} - {self.departamento.nome}"
    
class Atividade(models.Model):
    

    STATUS_CHOICES = [
        ('progresso', 'Em Progresso'),
        ('concluida', 'Concluída'),
        ('aguardando', 'Aguardando Informações'),
        ('atrasada', 'Atrasada'),
    ]

    DIFICULDADE_CHOICES = [
        ('facil', 'Fácil'),
        ('media', 'Média'),
        ('dificil', 'Difícil'),
    ]

    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
    ]

    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='atividades_funcionario')
    tipo_atividade = models.ForeignKey(TipoAtividade, on_delete=models.CASCADE, null=True, blank=True, related_name='atividades_tipo')
    
    descricao = models.TextField()
    data = models.DateField(auto_now_add=True)
    prazo = models.DateTimeField(null=True, blank=True, help_text="Prazo para conclusão da atividade")
    hora_inicio = models.TimeField(default=datetime.now)
    hora_fim = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='progresso')
    observacoes = models.TextField(blank=True, null=True)
    dificuldade = models.CharField(max_length=10, choices=DIFICULDADE_CHOICES, default='media')
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='media')
    
    tempo_gasto = models.DurationField(null=True, blank=True, help_text="Tempo total gasto na atividade")

    def calcular_tempo_gasto(self):
        if self.hora_fim:
            # Combine with a fixed date
            data_fixa = datetime.now().date()  # Use the current date
            inicio = datetime.combine(data_fixa, self.hora_inicio)
            fim = datetime.combine(data_fixa, self.hora_fim)

            # Return the difference
            return fim - inicio
        return timedelta()

    def __str__(self):
        return f"{self.funcionario.nome_completo} - {self.tipo_atividade} ({self.status})"

    def save(self, *args, **kwargs):
        # Calcular automaticamente o tempo gasto ao salvar, caso a atividade esteja concluída
        if self.status == 'concluida' and self.hora_fim:
            self.tempo_gasto = self.calcular_tempo_gasto()
            
        if self.tipo_atividade.departamento != self.funcionario.departamento:
            raise ValueError("O tipo de atividade deve pertencer ao mesmo departamento do funcionário.")


        # Definir como atrasada se passar do prazo
        if self.prazo and self.status != 'concluida' and timezone.now() > self.prazo:
            self.status = 'atrasada'

        super().save(*args, **kwargs)
