from audioop import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Departamento(models.Model):
    nome = models.CharField(max_length=65)
    
    def __str__(self):
        return self.nome
    

class Expedient(models.Model):
    numero_Ex = models.IntegerField()
    tipo = models.CharField(max_length=50)
    departamento = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    assunto = models.CharField(max_length=150, null=False, )
    prioridade = models.CharField(max_length=20)
    confidencial = models.BooleanField(default=False)
    descricao = models.TextField(null=True, )
    estado = models.CharField(max_length=20)
    anexo = models.FileField(upload_to ='expedient/uploads/%Y/%m/%d/', null=True,) 
    data_emissao = models.DateTimeField(auto_now_add=True)
    data_recepcao = models.DateTimeField(auto_now=True)
    recebido = models.BooleanField(default=False)
    slug = models.SlugField()
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, default=None)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.assunto
    
    def get_absolute_url(self):
        return reverse('expedients:expedient', args=(self.id,))
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.assunto)}'
            self.slug = slug
            
        return super().save(*args, **kwargs)
    
class Funcionario(models.Model):
    nome_completo = models.CharField(max_length=95)
    numero_telefone = models.CharField(max_length=65)
    estado = models.CharField(max_length=50)
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, default=None)
    
    def __str__(self):
        return self.nome_completo
