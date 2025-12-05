from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from vagas.models import Vaga, Candidatura
from empresa.models import Empresa
from usuarios.models import UsuarioAdaptado
from .forms import *
from django.core.paginator import Paginator
from django.views.generic import DetailView

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
        return redirect('empresa:painel_empresa')
    
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
    
    # vagas por area para estatisticas
    vagas_por_area = Vaga.objects.filter(ativo=True).values(
        'area'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
    # total de vagas
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
    total_usuarios = UsuarioAdaptado.objects.count()
    total_empresas = Empresa.objects.count()
    vagas_ativas = Vaga.objects.filter(ativo=True).count()
    total_candidaturas = Candidatura.objects.count()
    
    context = {
        'total_usuarios': total_usuarios,
        'total_empresas': total_empresas,
        'vagas_ativas': vagas_ativas,
        'total_candidaturas': total_candidaturas,
    }
    
    return render(request, 'admin/painel_admin.html', context)

@login_required
def minhas_candidaturas(request):
    candidaturas = Candidatura.objects.filter(
        usuario=request.user
    ).select_related('vaga', 'vaga__empresa').order_by('-data')
    
    context = {
        'candidaturas': candidaturas,
    }
    return render(request, 'usuarios/candidaturas.html', context)

def excluir_usuario(request, pk):
    usuario = get_object_or_404(UsuarioAdaptado, id=pk)
    nome_usuario = usuario.username
    
    if request.user == usuario:
        auth_logout(request)
        usuario.delete()
        messages.success(request, "Sua conta foi excluída com sucesso!")
        return redirect('home')  
    
    else:
        usuario.delete()
        messages.success(request, f"Usuário '{nome_usuario}' excluído com sucesso!")
        return redirect('usuarios:listar_usuarios') 

@login_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(UsuarioAdaptado, id=pk)
    
    if request.method == 'POST':
        formulario = UsuarioEditarForm(request.POST, request.FILES, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Usuário atualizado com sucesso!")
            
            if request.user == usuario:
                return redirect('usuarios:perfil_usuario')
            else:
                return redirect('admin:listar_usuarios')
    else:
        formulario = UsuarioEditarForm(instance=usuario)
    
    context = {
        'form': formulario,
        'usuario': usuario,
    }
    return render(request, 'usuarios/editar_usuario.html', context)

@login_required
def listar_usuarios(request):
    busca = request.GET.get('busca', '')
    tipo = request.GET.get('tipo', '')
    
    usuarios = UsuarioAdaptado.objects.all()
    
    if busca:
        usuarios = usuarios.filter(
            Q(username__icontains=busca) |
            Q(email__icontains=busca) |
            Q(first_name__icontains=busca) |
            Q(last_name__icontains=busca) |
            Q(cpf__icontains=busca)
        )
    
    if tipo == 'candidato':
        usuarios = usuarios.filter(is_admin=False, is_superuser=False)
    elif tipo == 'admin':
        usuarios = usuarios.filter(is_admin=True, is_superuser=False)
    elif tipo == 'superadmin':
        usuarios = usuarios.filter(is_superuser=True)
    
    usuarios = usuarios.order_by('-date_joined')
    
    # Paginação
    paginador = Paginator(usuarios, 10)
    pagina_numero = request.GET.get('pagina')
    objeto_pagina = paginador.get_page(pagina_numero)
    
    context = {
        'objeto_pagina': objeto_pagina,
        'busca': busca,
        'tipo': tipo,
        'total_usuarios': usuarios.count(),
    }
    return render(request, 'admin/listar_usuarios.html', context)

class UsuarioDetailView(DetailView):
    model = UsuarioAdaptado
    template_name = 'admin/detalhar_usuarios.html'
    context_object_name = 'usuario'



