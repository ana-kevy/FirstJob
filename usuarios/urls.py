from . import views
from django.urls import path, include
from usuarios.views import painel_candidato, painel_admin

app_name = "usuarios"

urlpatterns = [
    path("cadastro/", views.cadastrar_usuario, name="cadastrar_usuario"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("painel/candidato/", painel_candidato, name="painel_candidato"),
    path("admin/painel/", painel_admin, name="painel_admin"),
    path("perfil/", views.perfil_usuario, name="perfil_usuario"),
    path('minhas-candidaturas/', views.minhas_candidaturas, name='minhas_candidaturas'),
    path('excluir/<int:usuario_id>/', views.excluir_conta, name='excluir_conta'),
    path('editar/', views.editar_candidato, name='editar_candidato'),
    path('editar/<int:candidato_id>/', views.editar_candidato, name='editar_candidato_admin'),
]
