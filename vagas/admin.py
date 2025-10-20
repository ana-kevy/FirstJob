from django.contrib import admin
from .models import Vaga, Mensagem


@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'empresa', 'ativo', 'salario', 'data_publicacao')
    list_filter = ('ativo', 'empresa')
    search_fields = ('titulo', 'descricao', 'empresa__nome')
    ordering = ('-data_publicacao',)


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('candidato', 'empresa', 'conteudo_curto', 'data_envio')
    search_fields = ('candidato__username', 'empresa__nome', 'conteudo')
    ordering = ('-data_envio',)

    def conteudo_curto(self, obj):
        return obj.conteudo[:50] + ('...' if len(obj.conteudo) > 50 else '')
    conteudo_curto.short_description = 'Mensagem'

