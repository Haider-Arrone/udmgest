from django.db import models
from django.conf import settings

# Create your models here.
class Idioma(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome
    
class Curriculo(models.Model):
    REGIME_CONTRATO_CHOICES = [
        ('Indeterminado', 'Indeterminado'),
        ('Determinado', 'Determinado'),
    ]

    IDIOMA_CHOICES = [
        ('Português', 'Português'),
        ('Inglês', 'Inglês'),
        ('Francês', 'Francês'),
        ('Línguas Locais', 'Línguas Locais'),
        ('Outro', 'Outro'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="curriculo",
        verbose_name="Usuário",
        null=True,
        blank=True
    )

    # --- Campos principais ---
    cargo_actual = models.CharField(
        max_length=100,
        verbose_name="Cargo Actual",
        null=True,
        blank=True
    )
    regime_contrato = models.CharField(
        max_length=50,
        choices=REGIME_CONTRATO_CHOICES,
        verbose_name="Regime de Contrato",
        null=True,
        blank=True
    )
    data_nascimento = models.DateField(
        verbose_name="Data de Nascimento",
        null=True,
        blank=True
    )
    naturalidade = models.CharField(
        max_length=100,
        verbose_name="Naturalidade",
        null=True,
        blank=True
    )
    idiomas = models.ManyToManyField(
    Idioma,
    verbose_name="Idiomas",
    blank=True
)
    contacto_telefonico = models.CharField(
        max_length=50,
        verbose_name="Contacto Telefónico",
        null=True,
        blank=True
    )
    endereco_electronico = models.EmailField(
        verbose_name="Endereço Electrónico",
        null=True,
        blank=True
    )
    endereco_fisico = models.CharField(
        max_length=255,
        verbose_name="Endereço Físico",
        null=True,
        blank=True
    )
    areas_interesse = models.TextField(
        verbose_name="Áreas de Interesse",
        null=True,
        blank=True
    )

    ficheiro_cv = models.FileField(
        upload_to='cv/uploads/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name="Ficheiro do CV"
    )

    data_registo = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Registo"
    )

    class Meta:
        verbose_name = "Currículo"
        verbose_name_plural = "Currículos"
        ordering = ['user__username']

    def __str__(self):
        nome_usuario = self.user.get_full_name() if self.user else "Usuário não definido"
        return f"{nome_usuario} - {self.cargo_actual or 'Sem cargo definido'}"
    

class FormacaoAcademica(models.Model):
    GRAU_CHOICES = [
        ('Licenciatura', 'Licenciatura'),
        ('Mestrado', 'Mestrado'),
        ('Doutoramento', 'Doutoramento'),
        ('Técnico Médio', 'Técnico Médio'),
        ('Outro', 'Outro'),
    ]

    curriculo = models.ForeignKey(
        'Curriculo',
        on_delete=models.CASCADE,
        related_name='formacoes',
        verbose_name="Currículo",
        null=True,
        blank=True
    )

    grau_entrada = models.CharField(
        max_length=100,
        choices=GRAU_CHOICES,
        verbose_name="Grau Académico de Entrada",
        null=True,
        blank=True
    )
    grau_actual = models.CharField(
        max_length=100,
        choices=GRAU_CHOICES,
        verbose_name="Grau Académico Actual",
        null=True,
        blank=True
    )
    area_formacao = models.CharField(
        max_length=150,
        verbose_name="Área de Formação",
        null=True,
        blank=True
    )
    instituicao_ensino = models.CharField(
        max_length=150,
        verbose_name="Instituição de Ensino",
        null=True,
        blank=True
    )
    ano_conclusao = models.PositiveIntegerField(
        verbose_name="Ano de Conclusão",
        null=True,
        blank=True
    )

    data_registo = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Registo"
    )

    class Meta:
        verbose_name = "Formação Académica"
        verbose_name_plural = "Formações Académicas"
        ordering = ['-ano_conclusao']

    def __str__(self):
        return f"{self.area_formacao or 'Sem área'} - {self.instituicao_ensino or 'Sem instituição'}"
    
class CursoCertificacao(models.Model):
    curriculo = models.ForeignKey(
        'Curriculo',
        on_delete=models.CASCADE,
        related_name='cursos_certificacoes',
        verbose_name="Currículo",
        null=True,
        blank=True
    )

    nome_curso = models.CharField(
        max_length=150,
        verbose_name="Nome do Curso / Certificação",
        null=True,
        blank=True
    )
    instituicao_formadora = models.CharField(
        max_length=150,
        verbose_name="Instituição Formadora",
        null=True,
        blank=True
    )
    duracao = models.CharField(
        max_length=50,
        verbose_name="Duração",
        null=True,
        blank=True
    )
    ano_conclusao = models.PositiveIntegerField(
        verbose_name="Ano de Conclusão",
        null=True,
        blank=True
    )

    data_registo = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Registo"
    )

    class Meta:
        verbose_name = "Curso / Certificação"
        verbose_name_plural = "Cursos / Certificações"
        ordering = ['-ano_conclusao']

    def __str__(self):
        return f"{self.nome_curso or 'Sem nome'} - {self.instituicao_formadora or 'Sem instituição'}"

class CompetenciasDigitais(models.Model):
    NIVEL_CHOICES = [
        ('Básico', 'Básico'),
        ('Intermédio', 'Intermédio'),
        ('Avançado', 'Avançado'),
    ]

    SIM_NAO_CHOICES = [
        ('Sim', 'Sim'),
        ('Não', 'Não'),
    ]

    REDES_SOCIAIS_CHOICES = [
        ('Whatsapp', 'Whatsapp'),
        ('Instagram', 'Instagram'),
        ('Facebook', 'Facebook'),
        ('Twitter', 'Twitter'),
        ('LinkedIn', 'LinkedIn'),
    ]

    curriculo = models.ForeignKey(
        'Curriculo',
        on_delete=models.CASCADE,
        related_name='competencias_digitais',
        verbose_name="Currículo",
        null=True,
        blank=True
    )

    ferramentas_trabalho = models.CharField(
        max_length=50,
        choices=NIVEL_CHOICES,
        verbose_name="Uso de ferramentas de trabalho",
        null=True,
        blank=True
    )
    gestao_email = models.CharField(
        max_length=3,
        choices=SIM_NAO_CHOICES,
        verbose_name="Gestão de e-mail e comunicação digital",
        null=True,
        blank=True
    )
    uso_plataformas_ensino = models.CharField(
        max_length=3,
        choices=SIM_NAO_CHOICES,
        verbose_name="Uso de plataformas de ensino online",
        null=True,
        blank=True
    )
    plataforma_nome = models.CharField(
        max_length=100,
        verbose_name="Qual plataforma?",
        null=True,
        blank=True
    )
    uso_redes_sociais = models.CharField(
        max_length=50,
        choices=REDES_SOCIAIS_CHOICES,
        verbose_name="Uso de redes sociais",
        null=True,
        blank=True
    )
    outras_competencias = models.TextField(
        verbose_name="Outras competências digitais",
        null=True,
        blank=True
    )

    data_registo = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Registo"
    )

    class Meta:
        verbose_name = "Competência Digital"
        verbose_name_plural = "Competências Digitais"
        ordering = ['curriculo']

    def __str__(self):
        return f"{self.curriculo.user.get_full_name() if self.curriculo else 'Sem usuário'} - {self.ferramentas_trabalho or 'Sem nível definido'}"
    
class HabilidadesTalentos(models.Model):
    # Choices das categorias
    HABILIDADES_TECNICAS_CHOICES = [
        ('Marcenaria', 'Marcenaria'),
        ('Alfaiataria', 'Alfaiataria'),
        ('Mecânica', 'Mecânica'),
        ('Tecelagem e Bordado', 'Tecelagem e Bordado'),
        ('Cerâmica', 'Cerâmica'),
        ('Artesanato', 'Artesanato'),
    ]

    COMUNICACIONAIS_CHOICES = [
        ('Comunicação verbal', 'Comunicação verbal'),
        ('Comunicação escrita', 'Comunicação escrita'),
        ('Escuta activa', 'Escuta activa'),
        ('Negociação e persuasão', 'Negociação e persuasão'),
    ]

    CULTURAIS_CHOICES = [
        ('Canto', 'Canto'),
        ('Dança', 'Dança'),
        ('Teatro', 'Teatro'),
        ('Literatura oral', 'Literatura oral'),
        ('Artes visuais', 'Artes visuais'),
        ('Uso de instrumentos musicais', 'Uso de instrumentos musicais'),
    ]

    DESPORTIVAS_CHOICES = [
        ('Futebol', 'Futebol'),
        ('Basquetebol', 'Basquetebol'),
        ('Voleibol', 'Voleibol'),
        ('Andebol', 'Andebol'),
        ('Atletismo', 'Atletismo'),
        ('Ténis', 'Ténis'),
        ('Natação', 'Natação'),
        ('Caraté', 'Caraté'),
        ('Judo', 'Judo'),
        ('Xadrez', 'Xadrez'),
        ('Golfe', 'Golfe'),
    ]

    GASTRONOMICAS_CHOICES = [
        ('Culinária local', 'Culinária local'),
        ('Culinária rápida/fast food', 'Culinária rápida/fast food'),
        ('Culinária saudável', 'Culinária saudável'),
        ('Gastronomia nacional', 'Gastronomia nacional'),
        ('Gastronomia internacional', 'Gastronomia internacional'),
        ('Confeitaria e Panificação', 'Confeitaria e Panificação'),
        ('Organização de eventos', 'Organização de eventos'),
    ]

    # Associação ao currículo
    curriculo = models.ForeignKey(
        'Curriculo',
        on_delete=models.CASCADE,
        related_name='habilidades_talentos',
        verbose_name="Currículo",
        null=True,
        blank=True
    )

    # Campos para cada categoria
    habilidades_tecnicas = models.CharField(
        max_length=100,
        choices=HABILIDADES_TECNICAS_CHOICES,
        verbose_name="Habilidades Técnicas",
        null=True,
        blank=True
    )
    habilidades_tecnicas_outro = models.CharField(
        max_length=100,
        verbose_name="Outro (Habilidades Técnicas)",
        null=True,
        blank=True
    )

    comunicacionais = models.CharField(
        max_length=100,
        choices=COMUNICACIONAIS_CHOICES,
        verbose_name="Habilidades Comunicacionais",
        null=True,
        blank=True
    )
    comunicacionais_outro = models.CharField(
        max_length=100,
        verbose_name="Outro (Comunicacionais)",
        null=True,
        blank=True
    )

    culturais = models.CharField(
        max_length=100,
        choices=CULTURAIS_CHOICES,
        verbose_name="Habilidades Culturais",
        null=True,
        blank=True
    )
    culturais_outro = models.CharField(
        max_length=100,
        verbose_name="Outro (Culturais)",
        null=True,
        blank=True
    )

    desportivas = models.CharField(
        max_length=100,
        choices=DESPORTIVAS_CHOICES,
        verbose_name="Habilidades Desportivas",
        null=True,
        blank=True
    )
    gastronomicas = models.CharField(
        max_length=100,
        choices=GASTRONOMICAS_CHOICES,
        verbose_name="Habilidades Gastronômicas / Eventos",
        null=True,
        blank=True
    )
    outras_habilidades = models.TextField(
        verbose_name="Outras Habilidades e Talentos",
        null=True,
        blank=True
    )

    data_registo = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Registo"
    )

    class Meta:
        verbose_name = "Habilidade / Talento"
        verbose_name_plural = "Habilidades e Talentos"
        ordering = ['curriculo']

    def __str__(self):
        return f"{self.curriculo.user.get_full_name() if self.curriculo else 'Sem usuário'} - {self.habilidades_tecnicas or 'Sem habilidade definida'}"
    
class MobilidadeInterna(models.Model):
    SIM_NAO_CHOICES = [
        ('Sim', 'Sim'),
        ('Não', 'Não'),
    ]

    curriculo = models.ForeignKey(
        'Curriculo',
        on_delete=models.CASCADE,
        related_name='mobilidade_interna',
        verbose_name="Currículo",
        null=True,
        blank=True
    )

    disponibilidade = models.CharField(
        max_length=3,
        choices=SIM_NAO_CHOICES,
        verbose_name="Disponibilidade para mobilidade interna",
        null=True,
        blank=True
    )
    area_interesse = models.CharField(
        max_length=150,
        verbose_name="Área ou departamento de interesse",
        null=True,
        blank=True
    )
    experiencia_anterior = models.TextField(
        verbose_name="Experiência anterior em mobilidade interna",
        null=True,
        blank=True
    )

    data_registo = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Registo"
    )

    class Meta:
        verbose_name = "Mobilidade Interna"
        verbose_name_plural = "Mobilidade Interna"
        ordering = ['curriculo']

    def __str__(self):
        usuario = self.curriculo.user.get_full_name() if self.curriculo else "Sem usuário"
        return f"{usuario} - {self.disponibilidade or 'Sem disponibilidade definida'}"
