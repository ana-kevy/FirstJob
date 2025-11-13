from django.db import models
from empresa.models import Empresa
from usuarios.models import UsuarioAdaptado


class Vaga(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="vagas")
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    requisitos = models.TextField()
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    carga_horaria = models.TextField()
    ativo = models.BooleanField(default=True)
    data_publicacao = models.DateTimeField(auto_now_add=True)

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
    usuario = models.ForeignKey(UsuarioAdaptado, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "vaga")  #evita duplicada

    def __str__(self):
        return f"{self.usuario.username} -> {self.vaga.titulo}"
