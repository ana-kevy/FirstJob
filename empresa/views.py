from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Empresa
from .forms import EmpresaForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from vagas.models import Vaga, Candidatura

# Lista de empresas
class EmpresaListView(LoginRequiredMixin, ListView):
    model = Empresa
    template_name = "empresa/listar.html"
    context_object_name = "empresas"


# Detalhes de uma empresa
class EmpresaDetailView(LoginRequiredMixin, DetailView):
    model = Empresa
    template_name = "empresa/detalhe.html"
    context_object_name = "empresa"


# Criar nova empresa
class EmpresaCreateView(LoginRequiredMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = "empresa/form.html"
    success_url = reverse_lazy("empresa:listar_empresas")

    def dispatch(self, request, *args, **kwargs):
        # se já existir empresa, não deixa criar outra
        if hasattr(request.user, "empresa"):
            messages.warning(request, "Você já possui uma empresa cadastrada.")
            return redirect("empresa:listar_empresas")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        empresa = form.save(commit=False)
        empresa.usuario = self.request.user
        empresa.save()
        messages.success(self.request, "Empresa cadastrada com sucesso!")
        return redirect(self.success_url)


def cadastrar_empresa(request):
    """Cadastro de empresa"""
    if request.method == "POST":
        form = EmpresaForm(request.POST)
        if form.is_valid():
            empresa = form.save()

            messages.success(request, f"Empresa {empresa.nome} cadastrada com sucesso!")
            return redirect("usuarios:login")
    else:
        form = EmpresaForm()

    return render(request, "empresa/cadastrar.html", {"form": form})


# Editar empresa
class EmpresaUpdateView(LoginRequiredMixin, UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = "empresa/form.html"
    success_url = reverse_lazy("empresa:listar_empresas")

    def form_valid(self, form):
        messages.success(self.request, "Empresa atualizada com sucesso!")
        return super().form_valid(form)


# Excluir empresa
class EmpresaDeleteView(LoginRequiredMixin, DeleteView):
    model = Empresa
    template_name = "empresa/confirm_delete.html"
    success_url = reverse_lazy("empresa:listar_empresas")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Empresa excluída com sucesso!")
        return super().delete(request, *args, **kwargs)

# Listar vagas de uma empresa em especifico
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
    """Atualiza o status de uma candidatura"""
    candidatura = get_object_or_404(Candidatura, id=candidatura_id, vaga__empresa=request.user)
    candidatura.status = novo_status
    candidatura.save()
    
    messages.success(request, f'Status atualizado para {candidatura.get_status_display()}')
    return redirect('empresa:detalhar_vaga_empresa', vaga_id=candidatura.vaga.id)