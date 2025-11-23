from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UsuarioAdaptadoForm
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from vagas.models import Vaga
from usuarios.models import UsuarioAdaptado

@login_required
def perfil_usuario(request):
    usuario = request.user
    return render(request, "usuarios/perfil_usuario.html", {"usuario": usuario})

def criar_grupos(request):
    Group.objects.get_or_create(name="EMPRESA")
    Group.objects.get_or_create(name="USUARIO")
    return HttpResponse("Grupos criados")


# CADASTRO 
def cadastrar_usuario(request):
    if request.method == "POST":
        form = UsuarioAdaptadoForm(request.POST)
        if form.is_valid():
            user = form.save()

            messages.success(request, f"Cadastro de {user.username} realizado com sucesso!")
            return redirect("usuarios:login")
    else:
        form = UsuarioAdaptadoForm()

    return render(request, "usuarios/cadastrar.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect_to_painel_correto(request.user)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Bem-vindo, {user.username}!")
            return redirect_to_painel_correto(user)
        else:
            messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "usuarios/login.html")


def redirect_to_painel_correto(user):
    from empresa.models import Empresa

    if hasattr(user, 'is_admin_user') and user.is_admin_user:
        return redirect('usuarios:painel_admin')

    elif isinstance(user, Empresa):
        return redirect('usuarios:painel_empresa')
    
    else:
        return redirect('usuarios:painel_candidato')


def logout_view(request):
    auth_logout(request)
    messages.info(request, "Você saiu do sistema.")
    return redirect("usuarios:login")


# PAINÉIS 
@login_required
def painel_candidato(request):
    sete_dias_atras = timezone.now() - timedelta(days=7)
    vagas_recentes = Vaga.objects.filter(
        ativo=True, 
        data_publicacao__gte=sete_dias_atras
    ).order_by('-data_publicacao')[:6]
    
    # Vagas por area para estatisticas
    vagas_por_area = Vaga.objects.filter(ativo=True).values(
        'area'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
    # Total de vagas
    total_vagas = Vaga.objects.filter(ativo=True).count()

    vagas_por_area_ordenadas = sorted(vagas_por_area, key=lambda x: x['total'], reverse=True)

    context = {
        'vagas_recentes': vagas_recentes,
        'vagas_por_area': vagas_por_area,
        'total_vagas': total_vagas,
        'sete_dias_atras': sete_dias_atras,
        'vagas_por_area': vagas_por_area_ordenadas,
    }
    return render(request, 'usuarios/painel_candidato.html', context)

@login_required
def painel_empresa(request):
    context = {
        'empresa': request.user,
        'nome_empresa': request.user.nome, 
        'total_vagas': 0,
        'vagas_ativas': 0,
        'candidaturas_recentes': 0,
    }
    return render(request, 'empresa/painel_empresa.html', context)

@login_required
def painel_admin(request):
    return render(request, 'admin/painel_admin.html')