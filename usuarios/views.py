from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UsuarioAdaptadoForm
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from vagas.models import Vaga, Candidatura
from empresa.models import Empresa
from usuarios.models import UsuarioAdaptado
from .forms import *

@login_required
def perfil_usuario(request):
    usuario = request.user
    return render(request, "usuarios/perfil_usuario.html", {"usuario": usuario})

def criar_grupos(request):
    Group.objects.get_or_create(name="EMPRESA")
    Group.objects.get_or_create(name="USUARIO")
    return HttpResponse("Grupos criados")

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
        return redirect('/empresa/painel/')
    
    else:
        return redirect('usuarios:painel_candidato')

def logout_view(request):
    auth_logout(request)
    messages.info(request, "Você saiu do sistema.")
    return redirect("usuarios:login")

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
    total_empresas = Empresa.objects.count()

    vagas_por_area_ordenadas = sorted(vagas_por_area, key=lambda x: x['total'], reverse=True)

    context = {
        'vagas_recentes': vagas_recentes,
        'vagas_por_area': vagas_por_area,
        'total_vagas': total_vagas,
        'sete_dias_atras': sete_dias_atras,
        'vagas_por_area': vagas_por_area_ordenadas,
        'total_empresas': total_empresas,
    }
    return render(request, 'usuarios/painel_candidato.html', context)


@login_required
def painel_admin(request):
    return render(request, 'admin/painel_admin.html')


@login_required
def minhas_candidaturas(request):
    candidaturas = Candidatura.objects.filter(
        usuario=request.user
    ).select_related('vaga', 'vaga__empresa').order_by('-data')
    
    context = {
        'candidaturas': candidaturas,
    }
    return render(request, 'usuarios/candidaturas.html', context)

@login_required
def excluir_conta(request, usuario_id):
    usuario = get_object_or_404(UsuarioAdaptado, id=usuario_id)
    username = usuario.username
    usuario.delete()
    
    messages.success(request, f"Conta {username} excluída com sucesso!")
    return redirect('index')  


@login_required
def editar_candidato(request, candidato_id=None):
    if candidato_id:
        if not request.user.is_admin_user:
            messages.error(request, "Acesso não autorizado.")
            return redirect('usuarios:perfil_usuario')
        candidato = get_object_or_404(UsuarioAdaptado, id=candidato_id)
    else:
        candidato = request.user

    if request.method == 'POST':
        form = EditarCandidatoForm(request.POST, request.FILES, instance=candidato)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('usuarios:perfil_usuario')
    else:
        form = EditarCandidatoForm(instance=candidato)
    
    return render(request, 'usuarios/editar_usuario.html', {'form': form})