from django.contrib.auth.models import AbstractUser
from django.db import models

class UsuarioAdaptado(AbstractUser):
    cpf = models.CharField(max_length=14, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    curriculo = models.FileField(upload_to='curriculos/', blank=True, null=True)
    habilidades = models.TextField(blank=True, null=True)
    link_portfolio = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    @property
    def is_empresa_user(self):
        return False
    
    @property
    def is_candidato_user(self):
        return not self.is_admin  # Se não for admin, é candidato
    
    @property
    def is_admin_user(self):
        return self.is_admin or self.is_superuser

    def __str__(self):
        return f"{self.username} - {self.cpf if self.cpf else 'sem CPF'}"

