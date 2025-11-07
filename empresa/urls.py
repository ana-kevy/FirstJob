from django.urls import path
from . import views

app_name = 'empresa'

urlpatterns = [
    path('', views.EmpresaListView.as_view(), name='listar_empresas'),
    path('cadastro/', views.cadastrar_empresa, name='cadastrar_empresa'),
    path('<int:pk>/', views.EmpresaDetailView.as_view(), name='detalhe_empresa'),
    path('nova/', views.EmpresaCreateView.as_view(), name='criar_empresa'),
    path('<int:pk>/editar/', views.EmpresaUpdateView.as_view(), name='editar_empresa'),
    path('<int:pk>/excluir/', views.EmpresaDeleteView.as_view(), name='excluir_empresa'),
]
