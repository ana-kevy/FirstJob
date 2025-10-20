from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Vaga, Mensagem
from .form import VagaForm, MensagemForm
from empresa.models import Empresa


# ========= LISTAGEM =========
def listar_vagas(request):
    """Lista todas as vagas ativas"""
    vagas = Vaga.objects.filter(ativo=True).order_by('-data_publicacao')
    paginator = Paginator(vagas, 6)  # 6 vagas por página
    page = request.GET.get('page')
    vagas_paginadas = paginator.get_page(page)
    return render(request, 'vagas/listar.html', {'vagas': vagas_paginadas})


# ========= DETALHE =========
def detalhar_vaga(request, vaga_id):
    """Exibe detalhes de uma vaga e permite enviar mensagem"""
    vaga = get_object_or_404(Vaga, id=vaga_id)
    mensagens = Mensagem.objects.filter(empresa=vaga.empresa).order_by('-data_envio')

    if request.method == 'POST':
        form = MensagemForm(request.POST)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.empresa = vaga.empresa
            mensagem.candidato = request.user
            mensagem.save()
            messages.success(request, 'Mensagem enviada com sucesso!')
            return redirect('vagas:detalhar_vaga', vaga_id=vaga.id)
    else:
        form = MensagemForm()

    return render(request, 'vagas/detalhar.html', {
        'vaga': vaga,
        'mensagens': mensagens,
        'form': form
    })


# ========= CRUD DE VAGAS (EMPRESA) =========
@login_required
def criar_vaga(request):
    """Apenas empresas podem criar vagas"""
    if not hasattr(request.user, 'empresa'):
        messages.error(request, 'Somente empresas podem cadastrar vagas.')
        return redirect('vagas:listar_vagas')

    if request.method == 'POST':
        form = VagaForm(request.POST)
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.empresa = request.user.empresa
            vaga.save()
            messages.success(request, 'Vaga criada com sucesso!')
            return redirect('vagas:listar_vagas')
    else:
        form = VagaForm()
    return render(request, 'vagas/criar.html', {'form': form})


@login_required
def editar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa__usuario=request.user)
    if request.method == 'POST':
        form = VagaForm(request.POST, instance=vaga)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vaga atualizada com sucesso!')
            return redirect('vagas:listar_vagas')
    else:
        form = VagaForm(instance=vaga)
    return render(request, 'vagas/editar.html', {'form': form, 'vaga': vaga})


@login_required
def excluir_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa__usuario=request.user)
    vaga.delete()
    messages.success(request, 'Vaga excluída com sucesso!')
    return redirect('vagas:listar_vagas')

