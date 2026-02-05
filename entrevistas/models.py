

# Create your models here.
from django.db import models


class EntrevistaEstudante(models.Model):
    # =========================
    # CHOICES
    # =========================
    GENERO_CHOICES = [
        ('F', 'Feminino'),
        ('M', 'Masculino'),
    ]

    FACULDADE_CHOICES = [
        ('FCES', 'Faculdade de Ciências Económicas e Sociais'),
        ('FCJ', 'Faculdade de Ciências Jurídicas'),
        ('FCT', 'Faculdade de Ciências Tecnológicas'),
    ]

    FAIXA_ETARIA_CHOICES = [
        ('16-35', '16 - 35 anos'),
        ('36-45', '36 - 45 anos'),
        ('46+', '46 anos ou mais'),
    ]

    SITUACAO_PROFISSIONAL_CHOICES = [
        ('ESTUDANTE', 'Estudante'),
        ('ESTUDANTE_TRABALHADOR', 'Estudante Trabalhador'),
    ]

    SEMESTRE_CHOICES = [
        (1, '1º'),
        (2, '2º'),
        (3, '3º'),
        (4, '4º'),
        (5, '5º'),
        (6, '6º'),
        (7, '7º'),
        (8, '8º'),
    ]

    SUPORTE_DESPESAS_CHOICES = [
        ('PROPRIO', 'Encargo Próprio'),
        ('ENCARREGADO', 'Encarregado'),
        ('BOLSA', 'Bolsa'),
        ('EMPRESTIMO', 'Empréstimo'),
        ('OUTRO', 'Outro'),
    ]

    # =========================
    # DADOS DO ESTUDANTE
    # =========================
    nome = models.CharField(max_length=150, null=True, blank=True)
    curso = models.CharField(max_length=150, null=True, blank=True)
    genero = models.CharField(
        max_length=10, null=True, blank=True
    )
    faculdade = models.CharField(
        max_length=15,  null=True, blank=True
    )
    faixa_etaria = models.CharField(
        max_length=5,  null=True, blank=True
    )
    situacao_profissional = models.CharField(
        max_length=30, 
        null=True, blank=True
    )
    semestre = models.PositiveSmallIntegerField(
         null=True, blank=True
    )
    bairro_residencia = models.CharField(
        max_length=100, null=True, blank=True
    )

    # =========================
    # MOTIVO DA ESCOLHA DO CURSO
    # =========================
    motivo_escolha_curso = models.CharField(
    max_length=50,  null=True, blank=True
)

    # =========================
    # MOTIVO DA ESCOLHA DA UDM
    # =========================
    motivo_escolha_udm = models.CharField(
    max_length=50,  null=True, blank=True
)

    # =========================
    # COMO CONHECEU A UDM
    # =========================
    como_conheceu_udm = models.CharField(
    max_length=50, null=True, blank=True
)

    # =========================
    # DESPESAS
    # =========================
    suporte_despesas = models.CharField(
        max_length=30, 
        null=True, blank=True
    )

    # =========================
    # EXPECTATIVAS E RECEIOS
    # =========================
    expectativas_curso = models.TextField(null=True, blank=True)
    receios_curso = models.TextField(null=True, blank=True)
    
    # 7. AVALIAÇÃO GERAL
    # (escala 1–10)
    # =========================
    avaliacao_apresentacao = models.PositiveSmallIntegerField(null=True, blank=True)
    avaliacao_conhecimento_curso = models.PositiveSmallIntegerField(null=True, blank=True)
    avaliacao_conhecimento_udm = models.PositiveSmallIntegerField(null=True, blank=True)
    avaliacao_fluencia_comunicativa = models.PositiveSmallIntegerField(null=True, blank=True)
    avaliacao_objetivos_pessoais = models.PositiveSmallIntegerField(null=True, blank=True)

    # =========================
    # 8. CONTACTOS
    # =========================
    contacto_estudante_telefone = models.CharField(max_length=20, null=True, blank=True)
    contacto_estudante_email = models.EmailField(null=True, blank=True)
    contacto_encarregado_telefone = models.CharField(max_length=20, null=True, blank=True)

    # =========================
    # 9. OBSERVAÇÕES
    # =========================
    observacoes = models.TextField(null=True, blank=True)
    entrevistado_por = models.CharField(max_length=150, null=True, blank=True)
    data_entrevista_por = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    estado = models.CharField(max_length=50, null=True, blank=True)
    escola = models.CharField(max_length=50, null=True, blank=True)
    

    # =========================
    # METADADOS
    # =========================
    data_entrevista = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = "Entrevista do Estudante"
        verbose_name_plural = "Entrevistas dos Estudantes"
        ordering = ['-data_entrevista']

    def __str__(self):
        return f"{self.nome or 'Sem nome'} - {self.curso or 'Sem curso'}"

   