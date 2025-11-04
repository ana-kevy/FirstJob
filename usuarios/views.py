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

            # Define flags automáticas conforme o tipo de usuário (caso não sejam definidas no save do form)
            if getattr(user, 'tipo_usuario', None) == 'empresa':
                user.is_empresa = True
                user.is_candidato = False
                user.is_admin = False
            else:
                user.is_empresa = False
                user.is_candidato = True
                user.is_admin = False

            user.save()
            messages.success(request, f'Cadastro de {user.username} realizado com sucesso!')
            return redirect('usuarios:login')
    else:
        form = UsuarioAdaptadoForm()

    return render(request, 'usuarios/cadastrar.html', {'form': form})


# ========= LOGIN / LOGOUT =========
def login_view(request):
    # se já autenticado, redireciona para o painel apropriado
    if request.user.is_authenticated:
        if getattr(request.user, 'is_empresa', False):
            return redirect('empresa:painel_empresa')
        else:
            return redirect('usuarios:painel_candidato')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # passar request é uma boa prática (algumas autenticações usam isso)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Bem-vindo, {user.username}!')

                # Redirecionamento conforme tipo
                if getattr(user, 'is_empresa', False):
                    return redirect('empresa:painel_empresa')
                elif getattr(user, 'is_candidato', False):
                    return redirect('usuarios:painel_candidato')
                elif getattr(user, 'is_admin', False):
                    # ajustar conforme sua URL de admin
                    return redirect('admin:index')

                # fallback
                return redirect('vagas:listar_vagas')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Formulário inválido. Verifique os dados.')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('usuarios:login')


# ======= PAINÉIS =======
@login_required
def painel_candidato(request):
    # aqui você pode passar dados como vagas disponíveis, etc.
    return render(request, 'usuarios/painel_candidato.html')


@login_required
def painel_empresa(request):
    if not hasattr(request.user, 'empresa'):
        messages.info(request, 'Cadastre sua empresa primeiro.')
        return redirect('empresa:criar_empresa')
    # aqui você pode passar vagas criadas, mensagens, etc.
    return render(request, 'empresa/painel_empresa.html')
