from . import views
from django.urls import path, include
from usuarios.views import painel_candidato, painel_empresa, painel_admin

app_name = "usuarios"

urlpatterns = [
    path("cadastro/", views.cadastrar_usuario, name="cadastrar_usuario"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("painel/candidato/", painel_candidato, name="painel_candidato"),
    path("painel/empresa/", painel_empresa, name="painel_empresa"),
    path("admin/painel/", painel_admin, name="painel_admin"),
    path("perfil/", views.perfil_usuario, name="perfil_usuario"),
]
