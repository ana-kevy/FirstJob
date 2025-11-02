from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Empresa
from .forms import EmpresaForm

# Lista de empresas
class EmpresaListView(LoginRequiredMixin, ListView):
    model = Empresa
    template_name = 'empresa/listar.html'
    context_object_name = 'empresas'


# Detalhes de uma empresa
class EmpresaDetailView(LoginRequiredMixin, DetailView):
    model = Empresa
    template_name = 'empresa/detalhe.html'
    context_object_name = 'empresa'


# Criar nova empresa
class EmpresaCreateView(LoginRequiredMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/form.html'
    success_url = reverse_lazy('empresa:listar_empresas')

    def form_valid(self, form):
        messages.success(self.request, "Empresa cadastrada com sucesso!")
        return super().form_valid(form)


# Editar empresa
class EmpresaUpdateView(LoginRequiredMixin, UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/form.html'
    success_url = reverse_lazy('empresa:listar_empresas')

    def form_valid(self, form):
        messages.success(self.request, "Empresa atualizada com sucesso!")
        return super().form_valid(form)


# Excluir empresa
class EmpresaDeleteView(LoginRequiredMixin, DeleteView):
    model = Empresa
    template_name = 'empresa/confirm_delete.html'
    success_url = reverse_lazy('empresa:listar_empresas')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Empresa excluída com sucesso!")
        return super().delete(request, *args, **kwargs)
