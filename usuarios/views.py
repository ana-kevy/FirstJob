from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from .models import UsuarioAdaptado
from .form import UsuarioAdaptadoForm, LoginForm, PerfilForm, UsuarioEditForm, UsuarioFiltroForm

# ========= CADASTRO =========
def cadastrar_usuario(request):
    """Cadastro normal de usuário (empresa ou candidato)"""
    if request.method == 'POST':
        form = UsuarioAdaptadoForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Cadastro de {user.username} realizado com sucesso!')
            return redirect('login')
    else:
        form = UsuarioAdaptadoForm()
    return render(request, 'usuarios/cadastrar.html', {'form': form})

# ========= LOGIN / LOGOUT =========
def login_view(request):
    if request.user.is_authenticated:
        return redirect('listar_vagas')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Bem-vindo, {user.username}!')

                # Redirecionamento conforme grupo
                if user.is_empresa():
                    return redirect('painel_empresa')
                elif user.is_candidato():
                    return redirect('listar_vagas')
                elif user.is_admin():
                    return redirect('listar_usuarios')
                return redirect('listar_vagas')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('login')