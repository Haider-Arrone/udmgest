from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms.entrevista_form import EntrevistaEstudanteForm
from django.contrib import messages
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
from django.db.models import Count, Avg

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
        escola = request.POST.get("escola", "").strip()

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
        # def to_int(valor):
        #     return int(valor) if valor and valor.isdigit() else None

        # avaliacao_apresentacao = to_int(request.POST.get("avaliacao_apresentacao"))
        # avaliacao_conhecimento_curso = to_int(request.POST.get("avaliacao_conhecimento_curso"))
        # avaliacao_conhecimento_udm = to_int(request.POST.get("avaliacao_conhecimento_udm"))
        # avaliacao_fluencia_comunicativa = to_int(request.POST.get("avaliacao_fluencia_comunicativa"))
        # avaliacao_objetivos_pessoais = to_int(request.POST.get("avaliacao_objetivos_pessoais"))

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
        # print(observacoes)
        # entrevistado_por = request.POST.get("entrevistado_por", "").strip()

        # if not entrevistado_por:
        #     return JsonResponse({
        #         "success": False,
        #         "message": "O campo 'Entrevistado por' é obrigatório."
        #     }, status=400)

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

            # avaliacao_apresentacao=avaliacao_apresentacao,
            # avaliacao_conhecimento_curso=avaliacao_conhecimento_curso,
            # avaliacao_conhecimento_udm=avaliacao_conhecimento_udm,
            # avaliacao_fluencia_comunicativa=avaliacao_fluencia_comunicativa,
            # avaliacao_objetivos_pessoais=avaliacao_objetivos_pessoais,

            contacto_estudante_telefone=contacto_estudante_telefone,
            contacto_estudante_email=contacto_estudante_email,
            contacto_encarregado_telefone=contacto_encarregado_telefone,

            observacoes=observacoes,
            estado='pendente',
            escola=escola,
            # entrevistado_por=entrevistado_por,
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
    FACULDADES = ['FCT', 'FCJ', 'FCES']
    ESTADOS = ['pendente', 'avaliado', 'anulada']
    # Pesquisa
    query = request.GET.get("q", "")
    if query:
        entrevistas = entrevistas.filter(
            Q(nome__icontains=query) |
            Q(curso__icontains=query) |
            Q(faculdade__icontains=query) |
            Q(bairro_residencia__icontains=query) |
            Q(contacto_estudante_telefone__icontains=query) |
            Q(contacto_estudante_email__icontains=query)
        )
    
    # 🎯 Filtro por estado
    estado = request.GET.get("estado", "")
    print(estado)
    if estado:
        print(estado)
        entrevistas = entrevistas.filter(estado__iexact=estado)

    # 🎓 Filtro por faculdade
    faculdade = request.GET.get("faculdade", "")
    if faculdade:
        entrevistas = entrevistas.filter(faculdade=faculdade)

    # Paginação
    paginator = Paginator(entrevistas, 10)  # 20 por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    

    context = {
        "entrevistas": page_obj,
        "page_obj": page_obj,
        "query": query,
        "funcionario": funcionario,
        "estado_selecionado": estado,
        "faculdade_selecionada": faculdade,
        "estados_opcoes": ESTADOS,
        "faculdades_opcoes": FACULDADES,
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
    
@csrf_exempt
def entrevista_interna(request):
    """
    Abre o template para criação de uma nova entrevista.
    """

    

    return render(
        request,
        "entrevistas/indexx_interno.html",
       
    )
@login_required(login_url='authors:login', redirect_field_name='next')
def estatisticas_entrevistas(request):
    try:
        funcionario = (
            Funcionario.objects
            .select_related('departamento')
            .filter(author=request.user)
            .first()
        )

        if not funcionario:
            raise Http404("Funcionário não encontrado")

        entrevistas = EntrevistaEstudante.objects.all()
        faculdade_filtro = request.GET.get("faculdade", "").strip()

        if faculdade_filtro:
            entrevistas = entrevistas.filter(faculdade__iexact=faculdade_filtro)

        # ======================
        # MÉDIAS (com fallback)
        # ======================
        medias = entrevistas.aggregate(
            media_apresentacao=Avg("avaliacao_apresentacao"),
            media_conhecimento_curso=Avg("avaliacao_conhecimento_curso"),
            media_conhecimento_udm=Avg("avaliacao_conhecimento_udm"),
            media_fluencia=Avg("avaliacao_fluencia_comunicativa"),
            media_objetivos=Avg("avaliacao_objetivos_pessoais"),
        )

        # Garantir que nenhuma média venha como None
        for key, value in medias.items():
            medias[key] = round(value, 1) if value else 0

        context = {
            "lista_faculdades": EntrevistaEstudante.objects.exclude(
    faculdade__isnull=True
).exclude(
    faculdade=""
).values_list("faculdade", flat=True).distinct().order_by("faculdade"),

"faculdade_selecionada": faculdade_filtro,
            "funcionario": funcionario,

            # ======================
            # GERAL
            # ======================
            "total_entrevistas": entrevistas.count(),

            **medias,

            # ======================
            # PERFIL DO ESTUDANTE
            # ======================
            "por_genero": entrevistas.exclude(
                genero__isnull=True
            ).exclude(
                genero=""
            ).values("genero").annotate(total=Count("id")).order_by("-total"),

            "por_faixa_etaria": entrevistas.exclude(
                faixa_etaria__isnull=True
            ).exclude(
                faixa_etaria=""
            ).values("faixa_etaria").annotate(total=Count("id")).order_by("-total"),

            "por_situacao_profissional": entrevistas.exclude(
                situacao_profissional__isnull=True
            ).exclude(
                situacao_profissional=""
            ).values("situacao_profissional").annotate(total=Count("id")).order_by("-total"),

            "por_faculdade": entrevistas.exclude(
                faculdade__isnull=True
            ).exclude(
                faculdade=""
            ).values("faculdade").annotate(total=Count("id")).order_by("-total"),

            "por_curso": entrevistas.exclude(
                curso__isnull=True
            ).exclude(
                curso=""
            ).values("curso").annotate(total=Count("id")).order_by("-total")[:10],

            # ======================
            # DESPESAS
            # ======================
            "por_suporte_despesas": entrevistas.exclude(
                suporte_despesas__isnull=True
            ).exclude(
                suporte_despesas=""
            ).values("suporte_despesas").annotate(total=Count("id")).order_by("-total"),

            # ======================
            # MOTIVAÇÕES
            # ======================
            "motivo_escolha_curso": entrevistas.exclude(
                motivo_escolha_curso__isnull=True
            ).exclude(
                motivo_escolha_curso=""
            ).values("motivo_escolha_curso").annotate(total=Count("id")).order_by("-total"),

            "motivo_escolha_udm": entrevistas.exclude(
                motivo_escolha_udm__isnull=True
            ).exclude(
                motivo_escolha_udm=""
            ).values("motivo_escolha_udm").annotate(total=Count("id")).order_by("-total"),

            "como_conheceu_udm": entrevistas.exclude(
                como_conheceu_udm__isnull=True
            ).exclude(
                como_conheceu_udm=""
            ).values("como_conheceu_udm").annotate(total=Count("id")).order_by("-total"),
        }

        return render(request, "entrevistas/estatistica.html", context)

    except Http404:
        raise

    except Exception as e:
        logger.exception("Erro ao gerar estatísticas de entrevistas")
        raise Http404("Não foi possível carregar as estatísticas no momento.")
    
    
@login_required(login_url='authors:login', redirect_field_name='next')
def estatisticas_entrevistas_grafico(request):
    """
    Exibe estatísticas das entrevistas com gráficos interativos.
    """
    try:
        funcionario = (
            Funcionario.objects
            .select_related('departamento')
            .filter(author=request.user)
            .first()
        )
        if not funcionario:
            raise Http404("Funcionário não encontrado")

        entrevistas = EntrevistaEstudante.objects.all()
        
        faculdade_filtro = request.GET.get("faculdade", "").strip()

        if faculdade_filtro:
            entrevistas = entrevistas.filter(faculdade__iexact=faculdade_filtro)

        # ======================
        # MÉDIAS
        # ======================
        medias = entrevistas.aggregate(
            media_apresentacao=Avg("avaliacao_apresentacao"),
            media_conhecimento_curso=Avg("avaliacao_conhecimento_curso"),
            media_conhecimento_udm=Avg("avaliacao_conhecimento_udm"),
            media_fluencia=Avg("avaliacao_fluencia_comunicativa"),
            media_objetivos=Avg("avaliacao_objetivos_pessoais"),
        )
        # Garantir valores
        for key, value in medias.items():
            medias[key] = round(value, 1) if value else 0

        # ======================
        # DISTRIBUIÇÕES PARA GRÁFICOS
        # ======================
        def chart_data(queryset, field_name):
            """
            Retorna labels e valores para gráficos.
            """
            labels = []
            values = []
            for item in queryset:
                labels.append(item[field_name] if item[field_name] else "Não informado")
                values.append(item["total"])
            return labels, values

        # Perfil dos estudantes
        por_genero = entrevistas.exclude(genero__isnull=True).exclude(genero="").values("genero").annotate(total=Count("id")).order_by("-total")
        por_faixa_etaria = entrevistas.exclude(faixa_etaria__isnull=True).exclude(faixa_etaria="").values("faixa_etaria").annotate(total=Count("id")).order_by("-total")
        por_situacao_profissional = entrevistas.exclude(situacao_profissional__isnull=True).exclude(situacao_profissional="").values("situacao_profissional").annotate(total=Count("id")).order_by("-total")
        por_faculdade = entrevistas.exclude(faculdade__isnull=True).exclude(faculdade="").values("faculdade").annotate(total=Count("id")).order_by("-total")[:10]
        por_curso = entrevistas.exclude(curso__isnull=True).exclude(curso="").values("curso").annotate(total=Count("id")).order_by("-total")[:10]
        por_suporte_despesas = entrevistas.exclude(suporte_despesas__isnull=True).exclude(suporte_despesas="").values("suporte_despesas").annotate(total=Count("id")).order_by("-total")

        # Dados para gráficos
        genero_labels, genero_values = chart_data(por_genero, "genero")
        faixa_labels, faixa_values = chart_data(por_faixa_etaria, "faixa_etaria")
        situacao_labels, situacao_values = chart_data(por_situacao_profissional, "situacao_profissional")
        faculdade_labels, faculdade_values = chart_data(por_faculdade, "faculdade")
        curso_labels, curso_values = chart_data(por_curso, "curso")
        despesas_labels, despesas_values = chart_data(por_suporte_despesas, "suporte_despesas")
        
        lista_faculdades = EntrevistaEstudante.objects.exclude(
    faculdade__isnull=True
).exclude(
    faculdade=""
).values_list("faculdade", flat=True).distinct().order_by("faculdade")

        context = {
            "lista_faculdades": lista_faculdades,
    "faculdade_selecionada": faculdade_filtro,
            
            "funcionario": funcionario,
            "total_entrevistas": entrevistas.count(),
            **medias,

            # Dados gráficos
            "genero_labels": genero_labels,
            "genero_values": genero_values,

            "faixa_labels": faixa_labels,
            "faixa_values": faixa_values,

            "situacao_labels": situacao_labels,
            "situacao_values": situacao_values,

            "faculdade_labels": faculdade_labels,
            "faculdade_values": faculdade_values,

            "curso_labels": curso_labels,
            "curso_values": curso_values,

            "despesas_labels": despesas_labels,
            "despesas_values": despesas_values,
        }

        return render(request, "entrevistas/graficos.html", context)

    except Http404:
        raise
    except Exception as e:
        logger.exception("Erro ao gerar estatísticas em gráfico")
        raise Http404("Não foi possível carregar as estatísticas no momento.")
    
    
@login_required(login_url='authors:login', redirect_field_name='next')
def editar_avaliacao_entrevista(request, entrevista_id):
    """
    Edita apenas os dados de avaliação da entrevista (template estático).
    """

    # =========================
    # FUNCIONÁRIO LOGADO
    # =========================
    funcionario = (
        Funcionario.objects
        .filter(author=request.user)
        .select_related("departamento")
        .first()
    )

    if not funcionario:
        messages.error(
            request,
            "Não foi possível identificar o funcionário associado à sua conta."
        )
        raise Http404("Funcionário não encontrado")

    # =========================
    # ENTREVISTA
    # =========================
    entrevista = get_object_or_404(
        EntrevistaEstudante,
        id=entrevista_id
    )

    # =========================
    # SUBMISSÃO
    # =========================
    if request.method == "POST":
        try:
            # Campos esperados (escala 1–10)
            campos_avaliacao = [
                "avaliacao_apresentacao",
                "avaliacao_conhecimento_curso",
                "avaliacao_conhecimento_udm",
                "avaliacao_fluencia_comunicativa",
                "avaliacao_objetivos_pessoais",
            ]

            for campo in campos_avaliacao:
                valor = request.POST.get(campo)

                if valor:
                    valor_int = int(valor)
                    if valor_int < 1 or valor_int > 10:
                        raise ValueError(
                            f"Valor inválido para {campo}"
                        )
                    setattr(entrevista, campo, valor_int)
                else:
                    setattr(entrevista, campo, None)

            # Quem realizou/atualizou a avaliação
            entrevista.entrevistado_por = (
                funcionario.author.get_full_name()
                or funcionario.author.username
            )
            entrevista.estado = "avaliado"
            entrevista.data_entrevista_por = timezone.now()

            entrevista.save()

            messages.success(
                request,
                "Avaliação da entrevista actualizada com sucesso."
            )

            return redirect(
                "entrevistas:detalhes_entrevista",
                entrevista_id=entrevista.id
            )

        except ValueError:
            messages.error(
                request,
                "Foram detectados valores inválidos. "
                "Certifique-se de que todas as avaliações estão entre 1 e 10."
            )

        except Exception:
            messages.error(
                request,
                "Ocorreu um erro inesperado ao guardar a avaliação. "
                "Por favor, tente novamente."
            )

    # =========================
    # CONTEXTO
    # =========================
    context = {
        "entrevista": entrevista,
        "funcionario": funcionario,
    }

    return render(
        request,
        "entrevistas/avaliar_entrevista.html",
        context
    )
    
    
@login_required(login_url='authors:login', redirect_field_name='next')
def anular_entrevista(request, entrevista_id):
    """
    Marca a entrevista como ANULADA (soft delete).
    """

    funcionario = (
        Funcionario.objects
        .filter(author=request.user)
        .first()
    )

    if not funcionario:
        messages.error(
            request,
            "Não foi possível identificar o funcionário."
        )
        raise Http404("Funcionário não encontrado")

    entrevista = get_object_or_404(
        EntrevistaEstudante,
        id=entrevista_id
    )

    # Evitar dupla anulação
    if entrevista.estado == "ANULADA":
        messages.warning(
            request,
            "Esta entrevista já se encontra anulada."
        )
        return redirect(
            "entrevistas:detalhes_entrevista",
            entrevista_id=entrevista.id
        )

    if request.method == "POST":
        try:
            entrevista.estado = "ANULADA"
            entrevista.entrevistado_por = (
                funcionario.author.get_full_name()
                or funcionario.author.username
            )
            entrevista.save()

            messages.success(
                request,
                "Entrevista anulada com sucesso."
            )

        except Exception:
            messages.error(
                request,
                "Ocorreu um erro ao anular a entrevista. "
                "Por favor, tente novamente."
            )

        return redirect(
            "entrevistas:listar_entrevistas"
        )

    # Se alguém tentar aceder por GET
    messages.error(
        request,
        "Operação inválida."
    )
    return redirect(
        "entrevistas:detalhes_entrevista",
        entrevista_id=entrevista.id
    )