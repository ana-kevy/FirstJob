from django.contrib import admin
from .models import Vaga


@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "empresa", "ativo", "salario", "data_publicacao")
    list_filter = ("ativo", "empresa")
    search_fields = ("titulo", "descricao", "empresa__nome")
    ordering = ("-data_publicacao",)


