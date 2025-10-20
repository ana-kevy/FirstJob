from django.urls import path
from . import views

app_name = 'empresa'

urlpatterns = [
    path('', views.listar_empresas, name='listar_empresas'),
    path('nova/', views.criar_empresa, name='criar_empresa'),
    path('<int:pk>/editar/', views.editar_empresa, name='editar_empresa'),
    path('<int:pk>/excluir/', views.excluir_empresa, name='excluir_empresa'),
]
