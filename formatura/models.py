from django.db import models
from django.utils import timezone
from expedient.models import Funcionario, Departamento
from django.contrib.auth.models import User
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