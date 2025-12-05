from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioAdaptado


@admin.register(UsuarioAdaptado)
class UsuarioAdaptadoAdmin(UserAdmin):
    model = UsuarioAdaptado

    # Colunas que aparecem na listagem
    list_display = ("username", "email", "cpf", "is_admin", "is_staff", "is_active")
    list_filter = ("is_admin", "is_staff", "is_active", "groups")
    search_fields = ("username", "email", "cpf")

    # Campos extras adicionados aos fieldsets padrão do Django
    fieldsets = UserAdmin.fieldsets + (
        (
            "Informações adicionais",
            {
                "fields": (
                    "cpf",
                    "endereco",
                    "curriculo",
                    "habilidades",
                    "link_portfolio",
                    "is_admin",
                ),
            },
        ),
    )

    # Campos exibidos ao criar um novo usuário via admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Informações adicionais",
            {
                "fields": (
                    "cpf",
                    "endereco",
                    "curriculo",
                    "habilidades",
                    "link_portfolio",
                    "is_admin",
                ),
            },
        ),
    )

    ordering = ("username",)
