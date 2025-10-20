from django.contrib import admin
from .models import Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'email', 'telefone', 'usuario')
    search_fields = ('nome', 'cnpj', 'email')
    list_filter = ('usuario__is_active',)
    ordering = ('nome',)

    fieldsets = (
        ('Informações da Empresa', {
            'fields': ('nome', 'cnpj', 'endereco', 'telefone', 'email', 'descricao')
        }),
        ('Vinculação com Usuário', {
            'fields': ('usuario',)
        }),
    )

