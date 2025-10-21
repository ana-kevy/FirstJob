from django.contrib.auth.models import AbstractUser
from django.db import models

class UsuarioAdaptado(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    curriculo = models.FileField(upload_to='curriculos/', blank=True, null=True)
    habilidades = models.TextField(blank=True, null=True)
    link_portfolio = models.CharField(max_length=255, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=20, choices=[('candidato', 'Candidato'), ('empresa', 'Empresa')], default='candidato')
    is_admin = models.BooleanField(default=False)
    is_empresa = models.BooleanField(default=False)
    is_candidato = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} - {self.cpf if self.cpf else 'sem CPF'}"

