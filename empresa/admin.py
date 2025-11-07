from django.contrib import admin
from .models import Empresa
from django.contrib.auth.admin import UserAdmin

@admin.register(Empresa)
class EmpresaAdmin(UserAdmin):
    # Campos a mostrar na lista
    list_display = ['username', 'email', 'nome', 'cnpj', 'is_active', 'date_joined']
    list_filter = ['is_active', 'date_joined']
    search_fields = ['username', 'email', 'nome', 'cnpj']
    
    # Campos a mostrar no formulário de edição
    fieldsets = UserAdmin.fieldsets + (
        ('Dados da Empresa', {
            'fields': ('nome', 'cnpj', 'endereco', 'telefone', 'descricao')
        }),
    )
    
    # Campos a mostrar no formulário de criação
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dados da Empresa', {
            'fields': ('email', 'nome', 'cnpj', 'endereco', 'telefone', 'descricao')
        }),
    )