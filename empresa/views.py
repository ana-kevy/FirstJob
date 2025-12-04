from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Empresa
from .forms import EmpresaForm, EmpresaEditarForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from vagas.models import Vaga, Candidatura
from usuarios.models import UsuarioAdaptado
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q



@login_required
def perfil_empresa(request):
    empresa = request.user
    
    context = {
        "empresa": empresa,
    }
    return render(request, "empresa/perfil_empresa.html", context)

@login_required
def painel_empresa(request):
    empresa = request.user
    total_vagas = Vaga.objects.filter(empresa=empresa).count()
    vagas_ativas = Vaga.objects.filter(empresa=empresa, ativo=True).count()
    
    data_limite = timezone.now() - timedelta(days=30)
    candidaturas_recentes = Candidatura.objects.filter(
        vaga__empresa=empresa, 
        data__gte=data_limite  
    ).count()
    
    atividades_recentes = []
    
    vagas_recentes = Vaga.objects.filter(
        empresa=empresa,
        data_publicacao__gte=timezone.now() - timedelta(days=7)
    )[:5]
    
    for vaga in vagas_recentes:
        atividades_recentes.append({
            'tipo': 'vaga_publicada',
            'descricao': f'Vaga "{vaga.titulo}" publicada',
            'data': vaga.data_publicacao,
            'icone': 'text-info'
        })
    
    candidaturas_novas = Candidatura.objects.filter(
        vaga__empresa=empresa,
        data__gte=timezone.now() - timedelta(days=7) 
    ).select_related('vaga')[:5]
    
    for candidatura in candidaturas_novas:
        atividades_recentes.append({
            'tipo': 'nova_candidatura',
            'descricao': f'Nova candidatura para "{candidatura.vaga.titulo}"',
            'data': candidatura.data,
            'icone': 'text-success'
        })
    
    atividades_recentes.sort(key=lambda x: x['data'], reverse=True)
    
    context = {
        "empresa": empresa,
        "total_vagas": total_vagas,
        "vagas_ativas": vagas_ativas,
        "candidaturas_recentes": candidaturas_recentes,
        "atividades_recentes": atividades_recentes[:5]  
    }
    return render(request, "empresa/painel_empresa.html", context)


def is_admin_user(user):
    return user.is_authenticated and (user.is_superuser or getattr(user, 'is_admin', False))

@user_passes_test(is_admin_user, login_url='/usuarios/login/')
def listar_empresas(request):
    empresas = Empresa.objects.all()
    
    # filtros
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    if search:
        empresas = empresas.filter(
            Q(nome__icontains=search) |
            Q(cnpj__icontains=search) |
            Q(email__icontains=search) |
            Q(username__icontains=search)
        )
    
    # ordenação
    empresas = empresas.order_by('-date_joined')
    
    # paginação
    paginator = Paginator(empresas, 10)  # 10 empresas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # contar vagas para cada empresa
    for empresa in page_obj:
        empresa.total_vagas = Vaga.objects.filter(empresa=empresa).count()
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'status': status,
        'total_empresas': empresas.count(),
    }
    return render(request, 'admin/listar_empresas.html', context)

class EmpresaDetailView(LoginRequiredMixin, DetailView):
    model = Empresa
    template_name = "admin/detalhar_empresas.html"
    context_object_name = "empresa"


def cadastrar_empresa(request):
    if request.method == "POST":
        form = EmpresaForm(request.POST)
        if form.is_valid():
            empresa = form.save()

            messages.success(request, f"Empresa {empresa.nome} cadastrada com sucesso!")
            return redirect("usuarios:login")
    else:
        form = EmpresaForm()

    return render(request, "empresa/cadastrar.html", {"form": form})

def editar_empresa(request, pk):
    empresa = get_object_or_404(Empresa, id=pk)
    
    if request.method == 'POST':
        form = EmpresaEditarForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, "Empresa atualizada com sucesso!")
            
            if request.user == empresa:
                return redirect('empresa:perfil_empresa')
            else:
                return redirect('empresa:listar_empresas')
    else:
        form = EmpresaEditarForm(instance=empresa)
    
    context = {
        'form': form,
        'empresa': empresa,
    }
    return render(request, 'empresa/form.html', context)


@login_required(login_url='/usuarios/login/')
def excluir_empresa(request, pk):
    empresa = get_object_or_404(Empresa, id=pk)
    
    if request.user == empresa:
        from django.contrib.auth import logout
        logout(request)
        empresa.delete()
        messages.success(request, "Sua conta foi excluída com sucesso!")
        return redirect('home')
    
    elif request.user.is_superuser or getattr(request.user, 'is_admin', False):
        nome = empresa.nome
        empresa.delete()
        messages.success(request, f"Empresa '{nome}' excluída com sucesso!")
        return redirect('empresa:listar_empresas')

def listar_vagas_empresa(request):
    vagas = Vaga.objects.filter(empresa=request.user).order_by('-data_publicacao')
    
    context = {
        'vagas': vagas,
        'empresa': request.user
    }
    return render(request, 'empresa/listar_vagas_empresa.html', context)

# detalhar vaga com candidatura, separei views de detalhar
@login_required
def detalhar_vaga_empresa(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa=request.user)
    candidaturas = Candidatura.objects.filter(vaga=vaga).select_related('usuario')
    
    context = {
        'vaga': vaga,
        'candidaturas': candidaturas,
        'empresa': request.user
    }
    return render(request, 'empresa/detalhar_vaga_empresa.html', context)

@login_required
def excluir_vaga_empresa(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa=request.user)
    
    if request.method == 'POST':
        titulo_vaga = vaga.titulo
        vaga.delete()
        messages.success(request, f'Vaga "{titulo_vaga}" excluída com sucesso!')
        return redirect('empresa:listar_vagas_empresa')
    
    return redirect('empresa:detalhar_vaga_empresa', vaga_id=vaga_id)

@login_required
def atualizar_status_candidatura(request, candidatura_id, novo_status):
    candidatura = get_object_or_404(Candidatura, id=candidatura_id, vaga__empresa=request.user)
    candidatura.status = novo_status
    candidatura.save()
    
    messages.success(request, f'Status atualizado para {candidatura.get_status_display()}')
    return redirect('empresa:detalhar_vaga_empresa', vaga_id=candidatura.vaga.id)

@login_required
def ver_perfil_candidato(request, candidato_id):
    candidato = get_object_or_404(UsuarioAdaptado, id=candidato_id)

    candidaturas_empresa = Candidatura.objects.filter(
        usuario=candidato,
        vaga__empresa=request.user 
    ).exists()
    
    if not candidaturas_empresa:
        messages.error(request, "Acesso não autorizado.")
        return redirect('empresa:listar_vagas_empresa')
    
    candidatura = Candidatura.objects.filter(
        usuario=candidato,
        vaga__empresa=request.user
    ).first()
    
    context = {
        'candidato': candidato,
        'empresa': request.user, 
        'vaga_id': candidatura.vaga.id if candidatura else None
    }
    return render(request, 'empresa/ver_perfil_candidato.html', context)

