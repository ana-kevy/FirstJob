from django.contrib import admin
from .models import Empresa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cnpj', 'email', 'telefone')
    search_fields = ('nome', 'cnpj', 'email')
    list_filter = ('nome',)
