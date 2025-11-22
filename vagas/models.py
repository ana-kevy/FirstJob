from django.db import models
from empresa.models import Empresa
from usuarios.models import UsuarioAdaptado


class Vaga(models.Model):
    AREA_CHOICES = [
        ('tecnologia', 'Tecnologia da Informação'),
        ('saude', 'Saúde'),
        ('educacao', 'Educação'),
        ('financas', 'Finanças e Contabilidade'),
        ('marketing', 'Marketing e Vendas'),
        ('rh', 'Recursos Humanos'),
        ('juridico', 'Jurídico'),
        ('engenharia', 'Engenharia'),
        ('design', 'Design e Criatividade'),
        ('administrativo', 'Administrativo'),
        ('atendimento', 'Atendimento ao Cliente'),
        ('logistica', 'Logística e Transporte'),
        ('producao', 'Produção e Indústria'),
        ('vendas', 'Vendas e Comercial'),
        ('comunicacao', 'Comunicação e Mídia'),
        ('meio_ambiente', 'Meio Ambiente'),
        ('pesquisa', 'Pesquisa e Desenvolvimento'),
        ('turismo', 'Turismo e Hotelaria'),
        ('outros', 'Outros'),
    ]
    
    TIPO_VAGA_CHOICES = [
        ('presencial', 'Presencial'),
        ('remoto', 'Remoto'),
        ('hibrido', 'Híbrido'),
    ]

    TIPO_CONTRATACAO_CHOICES = [
        ('clt', 'CLT'),
        ('pj', 'PJ'),
        ('estagio', 'Estágio'),
        ('jovem_aprendiz', 'Jovem Aprendiz'),
        ('freelancer', 'Freelancer'),
        ('tempo_determinado', 'Tempo Determinado'),
        ('autonomo', 'Autônomo'),
        ('trainee', 'Trainee'),
        ('voluntario', 'Voluntário'),
        ('outros', 'Outros'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="vagas")
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    requisitos = models.TextField()
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    carga_horaria = models.TextField()
    ativo = models.BooleanField(default=True)
    data_publicacao = models.DateTimeField(auto_now_add=True)
    area = models.CharField(
        max_length=50, 
        choices=AREA_CHOICES, 
        default='tecnologia',
        verbose_name="Área de Atuação"
    )
    tipo_vaga = models.CharField(
        max_length=20, 
        choices=TIPO_VAGA_CHOICES, 
        default='presencial'
    )
    tipo_contratacao = models.CharField(
        max_length=20,
        choices=TIPO_CONTRATACAO_CHOICES,
        default='clt',
        verbose_name="Tipo de Contratação"
    )

    def __str__(self):
        return self.titulo


class Mensagem(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    candidato = models.ForeignKey(UsuarioAdaptado, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidato.username} → {self.empresa.nome}: {self.conteudo[:30]}"


class Candidatura(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('entrevista', 'Chamado para entrevista'),
        ('rejeitado', 'Rejeitado'),
        ('contratado', 'Contratado'),
    ]
    
    usuario = models.ForeignKey(UsuarioAdaptado, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    class Meta:
        unique_together = ("usuario", "vaga")  #evita duplicada

    def __str__(self):
        return f"{self.usuario.username} -> {self.vaga.titulo}"
