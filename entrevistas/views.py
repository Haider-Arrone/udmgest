from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms.entrevista_form import EntrevistaEstudanteForm

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from .models import EntrevistaEstudante  # Ajuste se o modelo tiver outro nome
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from expedient.models import  Funcionario


from django.db import IntegrityError, DatabaseError
import logging

logger = logging.getLogger(__name__)

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, DatabaseError
from django.utils import timezone
import logging
from django.http import Http404
from .models import EntrevistaEstudante

logger = logging.getLogger(__name__)


@csrf_exempt
def cadastrar_entrevista(request):
    """
    Recebe os dados do formulário de entrevista e grava no banco de dados.
    Trabalha com campos únicos (radio) conforme o model.
    """

    if request.method != "POST":
        return HttpResponseBadRequest("Método não permitido. Utilize POST.")

    try:
        # =====================================================
        # DADOS DO ESTUDANTE (OBRIGATÓRIOS)
        # =====================================================
        nome = request.POST.get("nome", "").strip()
        curso = request.POST.get("curso", "").strip()
        genero = request.POST.get("genero", "").strip()
        faculdade = request.POST.get("faculdade", "").strip()

        if not all([nome, curso, genero, faculdade]):
            return JsonResponse({
                "success": False,
                "message": "Nome, curso, género e faculdade são obrigatórios."
            }, status=400)

        # =====================================================
        # DADOS DO ESTUDANTE (OPCIONAIS)
        # =====================================================
        faixa_etaria = request.POST.get("faixa_etaria", "").strip()
        situacao_profissional = request.POST.get("situacao_profissional", "").strip()
        bairro_residencia = request.POST.get("bairro_residencia", "").strip()

        semestre_raw = request.POST.get("semestre", "").strip()
        semestre = int(semestre_raw) if semestre_raw.isdigit() else None

        # =====================================================
        # MOTIVO DA ESCOLHA DO CURSO (RADIO)
        # =====================================================
        motivo_escolha_curso = request.POST.get("motivo_escolha_curso", "").strip()
        motivo_outro = request.POST.get("motivo_outro", "").strip()
        if motivo_escolha_curso == "OUTRO" and motivo_outro:
            motivo_escolha_curso = motivo_outro

        # =====================================================
        # MOTIVO DA ESCOLHA DA UDM (RADIO)
        # =====================================================
        motivo_escolha_udm = request.POST.get("motivo_escolha_udm", "").strip()
        escolha_udm_outro = request.POST.get("escolha_udm_outro", "").strip()
        if motivo_escolha_udm == "OUTRO" and escolha_udm_outro:
            motivo_escolha_udm = escolha_udm_outro

        # =====================================================
        # COMO CONHECEU A UDM (RADIO)
        # =====================================================
        como_conheceu_udm = request.POST.get("como_conheceu_udm", "").strip()
        conheceu_outro = request.POST.get("conheceu_outro", "").strip()
        if como_conheceu_udm == "OUTRO" and conheceu_outro:
            como_conheceu_udm = conheceu_outro

        # =====================================================
        # SUPORTE DAS DESPESAS (RADIO + OUTRO)
        # =====================================================
        suporte_despesas = request.POST.get("suporte_despesas", "").strip()
        suporte_despesas_outro = request.POST.get("suporte_despesas_outro", "").strip()
        print(suporte_despesas, ":sup print")
        print(suporte_despesas_outro, ":sup outr print")

        if suporte_despesas == "OUTRO" and suporte_despesas_outro:
            suporte_despesas = suporte_despesas_outro

        # =====================================================
        # EXPECTATIVAS E RECEIOS
        # =====================================================
        expectativas_curso = request.POST.get("expectativas_curso", "").strip()
        receios_curso = request.POST.get("receios_curso", "").strip()
        print(expectativas_curso, "expectativas")
        print(receios_curso, "receio")

        # =====================================================
        # AVALIAÇÕES (1–10)
        # =====================================================
        def to_int(valor):
            return int(valor) if valor and valor.isdigit() else None

        avaliacao_apresentacao = to_int(request.POST.get("avaliacao_apresentacao"))
        avaliacao_conhecimento_curso = to_int(request.POST.get("avaliacao_conhecimento_curso"))
        avaliacao_conhecimento_udm = to_int(request.POST.get("avaliacao_conhecimento_udm"))
        avaliacao_fluencia_comunicativa = to_int(request.POST.get("avaliacao_fluencia_comunicativa"))
        avaliacao_objetivos_pessoais = to_int(request.POST.get("avaliacao_objetivos_pessoais"))

        # =====================================================
        # CONTACTOS
        # =====================================================
        contacto_estudante_telefone = request.POST.get("contacto_estudante_telefone", "").strip()
        contacto_estudante_email = request.POST.get("contacto_estudante_email", "").strip()
        contacto_encarregado_telefone = request.POST.get("contacto_encarregado_telefone", "").strip()

        # =====================================================
        # OBSERVAÇÕES
        # =====================================================
        observacoes = request.POST.get("observacoes", "").strip()
        print(observacoes)
        entrevistado_por = request.POST.get("entrevistado_por", "").strip()

        if not entrevistado_por:
            return JsonResponse({
                "success": False,
                "message": "O campo 'Entrevistado por' é obrigatório."
            }, status=400)

        # =====================================================
        # CRIAÇÃO DO REGISTO
        # =====================================================
        entrevista = EntrevistaEstudante.objects.create(
            nome=nome,
            curso=curso,
            genero=genero,
            faculdade=faculdade,
            faixa_etaria=faixa_etaria,
            situacao_profissional=situacao_profissional,
            semestre=semestre,
            bairro_residencia=bairro_residencia,

            motivo_escolha_curso=motivo_escolha_curso,
            motivo_escolha_udm=motivo_escolha_udm,
            como_conheceu_udm=como_conheceu_udm,
            suporte_despesas=suporte_despesas,

            expectativas_curso=expectativas_curso,
            receios_curso=receios_curso,

            avaliacao_apresentacao=avaliacao_apresentacao,
            avaliacao_conhecimento_curso=avaliacao_conhecimento_curso,
            avaliacao_conhecimento_udm=avaliacao_conhecimento_udm,
            avaliacao_fluencia_comunicativa=avaliacao_fluencia_comunicativa,
            avaliacao_objetivos_pessoais=avaliacao_objetivos_pessoais,

            contacto_estudante_telefone=contacto_estudante_telefone,
            contacto_estudante_email=contacto_estudante_email,
            contacto_encarregado_telefone=contacto_encarregado_telefone,

            observacoes=observacoes,
            entrevistado_por=entrevistado_por,
            data_entrevista=timezone.now()
        )

        return JsonResponse({
            "success": True,
            "message": "Entrevista cadastrada com sucesso!",
            "entrevista_id": entrevista.id
        })

    except IntegrityError:
        logger.exception("Erro de integridade ao cadastrar entrevista")
        return JsonResponse({
            "success": False,
            "message": "Erro de integridade dos dados."
        }, status=500)

    except DatabaseError:
        logger.exception("Erro de base de dados")
        return JsonResponse({
            "success": False,
            "message": "Erro interno na base de dados."
        }, status=500)

    except Exception:
        logger.exception("Erro inesperado ao cadastrar entrevista")
        return JsonResponse({
            "success": False,
            "message": "Ocorreu um erro inesperado ao cadastrar a entrevista."
        }, status=500)


@login_required(login_url='authors:login', redirect_field_name='next')
def listar_entrevistas(request):
    """
    Lista entrevistas com pesquisa e paginação.
    """
    funcionario = Funcionario.objects.filter(author=request.user).first()
    if not funcionario:
        raise Http404("Funcionário não encontrado")

    entrevistas = EntrevistaEstudante.objects.all().order_by('-data_entrevista')

    # Pesquisa
    query = request.GET.get("q")
    if query:
        entrevistas = entrevistas.filter(
            Q(nome__icontains=query) |
            Q(curso__icontains=query) |
            Q(faculdade__icontains=query) |
            Q(bairro_residencia__icontains=query) |
            Q(contacto_estudante_telefone__icontains=query) |
            Q(contacto_estudante_email__icontains=query)
        )

    # Paginação
    paginator = Paginator(entrevistas, 10)  # 20 por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "entrevistas": page_obj,
        "page_obj": page_obj,
        "query": query,
        "funcionario": funcionario,
    }

    return render(request, "entrevistas/listar_entrevistas.html", context)

@login_required(login_url='authors:login', redirect_field_name='next')
def detalhes_entrevista(request, entrevista_id):
    """
    Mostra os detalhes completos de uma entrevista.
    """

    # Garantir que o utilizador está associado a um funcionário
    funcionario = (
        Funcionario.objects
        .select_related('departamento')
        .filter(author=request.user)
        .first()
    )

    if not funcionario:
        raise Http404("Funcionário não encontrado")

    # Buscar entrevista
    entrevista = get_object_or_404(
        EntrevistaEstudante.objects.select_related(),
        id=entrevista_id
    )

    context = {
        "entrevista": entrevista,
        "funcionario": funcionario,
    }

    return render(
        request,
        "entrevistas/detalhes_entrevista.html",
        context
    )
    
@csrf_exempt
def entrevista_externa(request):
    """
    Abre o template para criação de uma nova entrevista.
    """

    

    return render(
        request,
        "entrevistas/indexx.html",
       
    )