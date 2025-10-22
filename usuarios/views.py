from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UsuarioAdaptado
from .forms import UsuarioAdaptadoForm, LoginForm

# ========= CADASTRO =========
def cadastrar_usuario(request):
    """Cadastro de usuário (empresa ou candidato)"""
    if request.method == 'POST':
        form = UsuarioAdaptadoForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Define flags automáticas conforme o tipo de usuário
            if user.tipo_usuario == 'empresa':
                user.is_empresa = True
                user.is_admin = False
            else:
                user.is_empresa = False
                user.is_admin = False

            user.save()
            messages.success(request, f'Cadastro de {user.username} realizado com sucesso!')
            return redirect('usuarios:login')
    else:
        form = UsuarioAdaptadoForm()

    return render(request, 'usuarios/cadastrar.html', {'form': form})

# ========= LOGIN / LOGOUT =========
def login_view(request):
    if request.user.is_authenticated:
        return redirect('vagas:listar_vagas')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Bem-vindo, {user.username}!')

                # Redirecionamento conforme tipo
                if user.is_empresa:
                    return redirect('painel_empresa')
                elif user.is_candidato:
                    return redirect('vagas:listar_vagas')
                elif user.is_admin:
                    return redirect('') # reveer esse trecho aqui, se vai ser so admin ou is_canidato

                return redirect('vagas:listar_vagas')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('usuarios:login')


