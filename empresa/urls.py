from django.urls import path
from . import views

app_name = "empresa"

urlpatterns = [
    path("", views.EmpresaListView.as_view(), name="listar_empresas"),
    path("cadastro/", views.cadastrar_empresa, name="cadastrar_empresa"),
    path("<int:pk>/", views.EmpresaDetailView.as_view(), name="detalhe_empresa"),
    path("nova/", views.EmpresaCreateView.as_view(), name="criar_empresa"),
    path("<int:pk>/editar/", views.EmpresaUpdateView.as_view(), name="editar_empresa"),
    path('deletar/<int:pk>/', views.EmpresaDeleteView.as_view(), name="excluir_empresa"),
    path('vagas/<int:vaga_id>/', views.detalhar_vaga_empresa, name='detalhar_vaga_empresa'),
    path('vagas/', views.listar_vagas_empresa, name='listar_vagas_empresa'),
    path('vagas/<int:vaga_id>/excluir/', views.excluir_vaga_empresa, name='excluir_vaga'),
    path('candidatura/<int:candidatura_id>/status/<str:novo_status>/',views.atualizar_status_candidatura, name='atualizar_status_candidatura'),
    path("perfil/", views.perfil_empresa, name="perfil_empresa"),
    path('candidato/<int:candidato_id>/perfil/', views.ver_perfil_candidato, name='ver_perfil_candidato'),
    path('painel/', views.painel_empresa, name='painel_empresa'),
    path("painel/empresa/", views.painel_empresa, name="painel_empresa"),
]
