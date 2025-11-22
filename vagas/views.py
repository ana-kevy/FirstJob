from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from .models import Vaga, Mensagem, Candidatura
from .form import VagaForm, MensagemForm
from empresa.models import Empresa
from django import forms


def listar_vagas(request):
    filtro_titulo = request.GET.get("titulo", "")
    filtro_cidade = request.GET.get("cidade", "")
    filtro_modalidade = request.GET.get("modalidade", "")  # remoto/presencial
    filtro_area = request.GET.get("area", "")

    vagas = Vaga.objects.filter(ativo=True)

    if filtro_titulo:
        vagas = vagas.filter(titulo__icontains=filtro_titulo)

    if filtro_cidade:
        vagas = vagas.filter(cidade__icontains=filtro_cidade)

    if filtro_modalidade:
        vagas = vagas.filter(modalidade__icontains=filtro_modalidade)

    if filtro_area:
        vagas = vagas.filter(area__icontains=filtro_area)

    vagas = vagas.order_by("-data_publicacao")

    # paginação
    paginator = Paginator(vagas, 6)
    page = request.GET.get("page")
    vagas_paginadas = paginator.get_page(page)

    contexto = {
        "vagas": vagas_paginadas,
        "filtro_titulo": filtro_titulo,
        "filtro_cidade": filtro_cidade,
        "filtro_modalidade": filtro_modalidade,
        "filtro_area": filtro_area,
    }

    return render(request, "vagas/listar.html", contexto)


def detalhar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    mensagens = Mensagem.objects.filter(empresa=vaga.empresa).order_by("-data_envio")

    if request.method == "POST":
        form = MensagemForm(request.POST)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.empresa = vaga.empresa
            mensagem.candidato = request.user
            mensagem.save()
            messages.success(request, "Mensagem enviada com sucesso!")
            return redirect("vagas:detalhar_vaga", vaga_id=vaga.id)
    else:
        form = MensagemForm()

    return render(
        request, "vagas/detalhar.html", {"vaga": vaga, "mensagens": mensagens, "form": form}
    )


def grupo_required(nome_grupo):
    def check(user):
        return user.is_authenticated and user.groups.filter(name=nome_grupo).exists()

    return user_passes_test(check)


def criar_vaga(request):
    if request.method == "POST":
        form = VagaForm(request.POST)
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.empresa = request.user  
            vaga.save()
            messages.success(request, "Vaga criada com sucesso!")
            return redirect("usuarios:painel_empresa")  
    else:
        form = VagaForm()
    
    return render(request, "vagas/criar.html", {"form": form})

@login_required
def editar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa=request.user)
    if request.method == "POST":
        form = VagaForm(request.POST, instance=vaga)
        if form.is_valid():
            form.save()
            messages.success(request, "Vaga atualizada com sucesso!")
            return redirect("empresa:listar_vagas_empresa")
    else:
        form = VagaForm(instance=vaga)
    return render(request, "vagas/editar.html", {"form": form, "vaga": vaga})


@login_required
def excluir_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa__usuario=request.user)
    vaga.delete()
    messages.success(request, "Vaga excluída com sucesso!")
    return redirect("vagas:listar_vagas")


@login_required
def candidatar(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)

    if Candidatura.objects.filter(usuario=request.user, vaga=vaga).exists():
        messages.warning(request, "Você já se candidatou nessa vaga.")
        return redirect("vagas:detalhar_vaga", vaga_id=vaga.id)

    Candidatura.objects.create(usuario=request.user, vaga=vaga)
    messages.success(request, "Candidatura realizada com sucesso!")
    return redirect("vagas:detalhar_vaga", vaga_id=vaga.id)
