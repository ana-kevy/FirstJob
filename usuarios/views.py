from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UsuarioAdaptado
from .forms import UsuarioAdaptadoForm, LoginForm
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm

def criar_grupos(request):
    Group.objects.get_or_create(name='EMPRESA')
    Group.objects.get_or_create(name='USUARIO')
    return HttpResponse("Grupos criados")

# ========= CADASTRO =========
def cadastrar_usuario(request):
    """Cadastro de usuário (apenas candidato agora)"""
    if request.method == 'POST':
        form = UsuarioAdaptadoForm(request.POST)
        if form.is_valid():
            user = form.save()

            messages.success(request, f'Cadastro de {user.username} realizado com sucesso!')
            return redirect('usuarios:login')
    else:
        form = UsuarioAdaptadoForm()

    return render(request, 'usuarios/cadastrar.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect_to_painel_correto(request.user)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            from django.contrib.auth import login as auth_login
            auth_login(request, user)
            messages.success(request, f'Bem-vindo, {user.username}!')
            return redirect_to_painel_correto(user)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'usuarios/login.html')

def redirect_to_painel_correto(user):
    """Redirecionamento melhorado"""
    print(f"DEBUG - Redirecionando usuário: {user.username}")
    print(f"DEBUG - Model name: {user._meta.model_name}")
    
    # Método 1: Por instância
    from empresa.models import Empresa
    if isinstance(user, Empresa):
        print("DEBUG - Redirecionando para EMPRESA (por instância)")
        return redirect('usuarios:painel_empresa')
    
    # Método 2: Por nome do modelo
    elif user._meta.model_name == 'empresa':
        print("DEBUG - Redirecionando para EMPRESA (por model_name)")
        return redirect('usuarios:painel_empresa')
    
    # Método 3: Por campo específico
    elif hasattr(user, 'cnpj'):
        print("DEBUG - Redirecionando para EMPRESA (por campo cnpj)")
        return redirect('usuarios:painel_empresa')
    
    else:
        print("DEBUG - Redirecionando para CANDIDATO")
        return redirect('usuarios:painel_candidato')

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
    return render(request, 'empresa/painel_empresa.html')

@login_required
def painel_admin(request):
    if not request.user.is_admin_user:
        from django.contrib import messages
        messages.error(request, "Acesso não autorizado.")
        return redirect('vagas:listar_vagas')
    return render(request, 'admin/painel_admin.html')



