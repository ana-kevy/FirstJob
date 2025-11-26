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
    filtro_empresa = request.GET.get("empresa", "")
    filtro_salario_min = request.GET.get("salario_min", "")
    filtro_area = request.GET.get("area", "")
    filtro_tipo_vaga = request.GET.get("tipo_vaga", "")
    filtro_tipo_contratacao = request.GET.get("tipo_contratacao", "")
    filtro_ativo = request.GET.get("ativo", "")

    vagas = Vaga.objects.all()

    if filtro_titulo:
        vagas = vagas.filter(titulo__icontains=filtro_titulo)

    if filtro_empresa:
        vagas = vagas.filter(empresa__nome__icontains=filtro_empresa)

    if filtro_salario_min:
        try:
            salario_min = float(filtro_salario_min)
            vagas = vagas.filter(salario__gte=salario_min)
        except ValueError:
            pass

    if filtro_area and filtro_area != "todas":
        vagas = vagas.filter(area=filtro_area)

    if filtro_tipo_vaga and filtro_tipo_vaga != "todas":
        vagas = vagas.filter(tipo_vaga=filtro_tipo_vaga)

    if filtro_tipo_contratacao and filtro_tipo_contratacao != "todas":
        vagas = vagas.filter(tipo_contratacao=filtro_tipo_contratacao)

    if filtro_ativo == "false":
        vagas = vagas.filter(ativo=False)
    else:
        vagas = vagas.filter(ativo=True)

    vagas = vagas.order_by("-data_publicacao")

    paginator = Paginator(vagas, 6)
    page = request.GET.get("page")
    vagas_paginadas = paginator.get_page(page)

    contexto = {
        "vagas": vagas_paginadas,
        "filtro_titulo": filtro_titulo,
        "filtro_empresa": filtro_empresa,
        "filtro_salario_min": filtro_salario_min,
        "filtro_area": filtro_area,
        "filtro_tipo_vaga": filtro_tipo_vaga,
        "filtro_tipo_contratacao": filtro_tipo_contratacao,
        "filtro_ativo": filtro_ativo,
        "areas": Vaga.AREA_CHOICES,
        "tipos_vaga": Vaga.TIPO_VAGA_CHOICES,
        "tipos_contratacao": Vaga.TIPO_CONTRATACAO_CHOICES,
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
