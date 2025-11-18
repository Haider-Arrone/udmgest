from django.db import models

# Create your models here.
class Event(models.Model):
    EVENT_TYPES = [
        ('holiday', 'Feriado'),
        ('exam', 'Exame'),
        ('class', 'Aula'),
        ('break', 'Interrupção'),
    ]

    title = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=EVENT_TYPES, null=True, blank=True)
    semester = models.CharField(max_length=20, null=True, blank=True)
    course = models.CharField(max_length=100, null=True, blank=True)
    turma = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title or "Evento sem título"