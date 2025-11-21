from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class Evento(models.Model):
    titulo = models.CharField(max_length=255, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    local = models.CharField(max_length=255, blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data"]

    def __str__(self):
        return self.titulo or "Evento sem título"


class Convite(models.Model):

    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        CONFIRMADO = "confirmado", "Confirmado"
        PRESENTE = "presente", "Presente"
        AUSENTE = "ausente", "Ausente"

    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name="convites",
        blank=True,
        null=True,
    )

    nome_completo = models.CharField(max_length=255, blank=True, null=True)
    contacto = models.CharField(max_length=50, blank=True, null=True)

    lugares_reservados = models.PositiveIntegerField(
        default=1,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
        blank=True,
        null=True
    )

    codigo_convite = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    codigo_estudante = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    presente_em = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Hora em que o convidado foi registado como presente"
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_completo or "Convite sem nome"

    def marcar_presenca(self):
        """Marca presença no evento"""
        self.status = self.Status.PRESENTE
        self.presente_em = timezone.now()
        self.save()
