from django.contrib.auth.models import AbstractUser
from django.db import models


class Empresa(AbstractUser):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    groups = models.ManyToManyField("auth.Group", related_name="empresa_set", blank=True)
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="empresa_set", blank=True
    )

    def __str__(self):
        return self.nome
