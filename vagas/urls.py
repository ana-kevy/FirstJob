from django.urls import path
from . import views

app_name = "vagas"

urlpatterns = [
    path("listar/", views.listar_vagas, name="listar_vagas"),
    path("<int:vaga_id>/", views.detalhar_vaga, name="detalhar_vaga"),
    path("criar/", views.criar_vaga, name="criar_vaga"),
    path("<int:vaga_id>/editar/", views.editar_vaga, name="editar_vaga"),
    path("<int:vaga_id>/excluir/", views.excluir_vaga, name="excluir_vaga"),
    path("<int:vaga_id>/candidatar/", views.candidatar, name="candidatar"),
]
