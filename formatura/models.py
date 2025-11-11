from django.db import models
from django.utils import timezone
from expedient.models import Funcionario, Departamento
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Presenca(models.Model):
    """
    Armazena os registos de presença dos funcionários provenientes do
    dispositivo biométrico Hikvision. Cada registo representa a hora
    de entrada de um funcionário num determinado dia.
    """

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='presencas',
        verbose_name="Funcionário",
        help_text="Funcionário que registou a presença no dispositivo biométrico.",
        null=True,
        blank=True,
    )

    data_presenca = models.DateField(
        verbose_name="Data da Presença",
        default=None,
        null=True,
        blank=True,
        help_text="Data em que o funcionário marcou a presença."
    )

    hora_entrada = models.TimeField(
        verbose_name="Hora de Entrada",
        null=True,
        blank=True,
        help_text="Hora exata em que o funcionário registou a presença."
    )

    origem_registo = models.CharField(
        max_length=50,
        default=None,
        null=True,
        blank=True,
        verbose_name="Origem do Registo",
        help_text="Origem do registo de presença (fixo: dispositivo biométrico Hikvision)."
    )

    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
        help_text="Data e hora em que o registo foi criado no sistema."
    )

    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em",
        help_text="Data e hora da última atualização do registo."
    )

    class Meta:
        verbose_name = "Presença"
        verbose_name_plural = "Presenças"
        ordering = ['-data_presenca', 'hora_entrada']
        indexes = [
            models.Index(fields=['usuario']),
            models.Index(fields=['data_presenca']),
        ]
        # Unique together removido, já que os campos podem ser nulos
        # unique_together = ('funcionario', 'data_presenca')

    def __str__(self):
        nome = self.usuario.get_full_name() if self.usuario else "—"
        data = self.data_presenca.strftime('%Y-%m-%d') if self.data_presenca else "Sem data"
        hora = self.hora_entrada.strftime('%H:%M') if self.hora_entrada else "Sem hora"
        return f"{nome} - {data} ({hora})"

    def is_atrasado(self, hora_limite="08:00"):
        """Verifica se o funcionário chegou após o horário definido (por padrão, 08:00)."""
        if not self.hora_entrada:
            return False
        limite = timezone.datetime.strptime(hora_limite, "%H:%M").time()
        return self.hora_entrada > limite
    
    
class TimeStampedModel(models.Model):
    """
    Abstract base model para auditoria temporal
    """
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Permite desativar registros sem apagá-los
    """
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True
        
class Formatura(TimeStampedModel, SoftDeleteModel):
    titulo = models.CharField(max_length=255, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    local = models.CharField(max_length=255, blank=True, null=True)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fim = models.TimeField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)  # detalhes gerais
    observacoes = models.TextField(blank=True, null=True)  # considerações finais ou instruções

    publicado = models.BooleanField(default=True)
    
    # Auditoria
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="formaturas_criado",
        on_delete=models.SET_NULL,
        verbose_name="Criado por"
    )
    atualizado_em = models.DateTimeField(auto_now=True)
    atualizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="formaturas_atualizado",
        on_delete=models.SET_NULL,
        verbose_name="Atualizado por"
    )


    class Meta:
        ordering = ["-data", "titulo"]
        verbose_name = "Formatura"
        verbose_name_plural = "Formaturas"

    def __str__(self):
        return f"{self.titulo or 'Sem título'} - {self.data or 'Sem data'} ({self.local or '-'})"

    @property
    def progresso_percentual(self):
        pontos = self.pontos_agenda.filter(ativo=True)
        if not pontos.exists():
            return 0
        return round(sum(p.percentual or 0 for p in pontos) / pontos.count(), 2)

    @property
    def total_tarefas(self):
        return self.pontos_agenda.filter(ativo=True).count()

    @property
    def tarefas_concluidas(self):
        return self.pontos_agenda.filter(
            ativo=True,
            status=PontoAgenda.Status.CONCLUIDA
        ).count()


class PontoAgenda(TimeStampedModel, SoftDeleteModel):
    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        EM_PROGRESSO = "em_progresso", "Em Progresso"
        CONCLUIDA = "concluida", "Concluída"
        ATRASADA = "atrasada", "Atrasada"

    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
    ]

    formatura = models.ForeignKey(
        Formatura,
        on_delete=models.CASCADE,
        related_name="pontos_agenda",
        blank=True,
        null=True
    )

    ordem = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
        help_text="Define a sequência de apresentação do ponto de agenda"
    )

    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pontos_agenda"
    )

    responsavel = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pontos_agenda"
    )

    titulo = models.CharField(max_length=255, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
        blank=True,
        null=True
    )
    prioridade = models.CharField(
        max_length=10,
        choices=PRIORIDADE_CHOICES,
        default='media',
        blank=True,
        null=True
    )

    data_limite = models.DateField(blank=True, null=True)
    percentual = models.PositiveIntegerField(default=0, blank=True, null=True)
    justificativa = models.TextField(blank=True, null=True)
    anexo = models.FileField(upload_to="formaturas/anexos/", null=True, blank=True)
    aprovado = models.BooleanField(default=False)
    comentario_avaliador = models.TextField(blank=True, null=True)
    
    # Auditoria
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="pontosagenda_criado",
        on_delete=models.SET_NULL,
        verbose_name="Criado por"
    )
    atualizado_em = models.DateTimeField(auto_now=True)
    atualizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="pontosagenda_atualizado",
        on_delete=models.SET_NULL,
        verbose_name="Atualizado por"
    )

    class Meta:
        ordering = ["ordem", "-prioridade", "titulo"]
        verbose_name = "Ponto de Agenda"
        verbose_name_plural = "Pontos de Agenda"

    def __str__(self):
        dep = f"{self.departamento.nome}" if self.departamento else "Sem departamento"
        resp = f"{self.responsavel.get_full_name()}" if self.responsavel else "Sem responsável"
        return f"[{self.ordem or '-'}] {self.titulo or 'Sem título'} | {dep} | {resp}"

    @property
    def atrasada(self):
        return (
            self.data_limite
            and self.data_limite < timezone.now().date()
            and self.status != self.Status.CONCLUIDA
        )

