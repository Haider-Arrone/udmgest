from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your models here.
class Profile(models.Model):
    nome_completo = models.CharField(max_length=95)
    numero_telefone = models.CharField(max_length=65)
    estudante_interno = models.BooleanField(default=False, null=True, )
    instituicao = models.CharField(max_length=100, null=True, )
    codigo_estudante = models.IntegerField(null=True, )
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome_completo
   