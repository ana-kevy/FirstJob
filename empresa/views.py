from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Empresa
from .forms import EmpresaForm

# Lista todas as empresas
@login_required
def listar_empresas(request):
    empresas = Empresa.objects.all()
    return render(request, 'empresa/listar_empresas.html', {'empresas': empresas})

# Cria uma nova empresa
@login_required
def criar_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa cadastrada com sucesso!')
            return redirect('empresa:listar_empresas')
    else:
        form = EmpresaForm()
    return render(request, 'empresa/criar_empresa.html', {'form': form})

# Edita uma empresa existente
@login_required
def editar_empresa(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa atualizada com sucesso!')
            return redirect('empresa:listar_empresas')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'empresa/editar_empresa.html', {'form': form, 'empresa': empresa})

# Exclui uma empresa
@login_required
def excluir_empresa(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        empresa.delete()
        messages.success(request, 'Empresa excluída com sucesso!')
        return redirect('empresa:listar_empresas')
    return render(request, 'empresa/excluir_empresa.html', {'empresa': empresa})

