from django.urls import path
from . import views

app_name = "empresa"

urlpatterns = [
    path("admin/listar/empresa", views.listar_empresas, name="listar_empresas"),
    path("detalhar/<int:pk>/", views.EmpresaDetailView.as_view(), name="detalhar_empresa"),
    path("<int:pk>/editar/", views.editar_empresa, name="editar_empresa"),

    path("cadastro/", views.cadastrar_empresa, name="cadastrar_empresa"),
    path('deletar/<int:pk>/', views.excluir_empresa, name="excluir_empresa"),

    path('vagas/<int:vaga_id>/', views.detalhar_vaga_empresa, name='detalhar_vaga_empresa'),
    path('vagas/', views.listar_vagas_empresa, name='listar_vagas_empresa'),
    path('vagas/<int:vaga_id>/excluir/', views.excluir_vaga_empresa, name='excluir_vaga'),
    path('candidatura/<int:candidatura_id>/status/<str:novo_status>/',views.atualizar_status_candidatura, name='atualizar_status_candidatura'),

    path("perfil/", views.perfil_empresa, name="perfil_empresa"),
    path('candidato/<int:candidato_id>/perfil/', views.ver_perfil_candidato, name='ver_perfil_candidato'),
    path("painel/empresa/", views.painel_empresa, name="painel_empresa"),
]
