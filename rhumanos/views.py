from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms.rhumanos_form import CurriculoForm, CompetenciasFormSet, CursoFormSet, HabilidadesFormSet, MobilidadeFormSet, FormacaoFormSet
from .models import Curriculo, Idioma
from expedient.models import Funcionario
from django.db import DatabaseError, IntegrityError, transaction
import logging
from django.db.models import Prefetch, Q
from django.core.paginator import Paginator
from .models import Curriculo, FormacaoAcademica, CursoCertificacao, CompetenciasDigitais, HabilidadesTalentos, MobilidadeInterna
from django.http import Http404, HttpRequest, HttpResponse
from utils.expedient.pagination import make_pagination

from .filters import CurriculoFilter
# Create your views here.
# Configura um logger para registrar erros
logger = logging.getLogger(__name__)

PER_PAGE = 10

@login_required(login_url='authors:login', redirect_field_name='next')
def cadastrar_curriculo(request):
    try:
        funcionario = get_object_or_404(Funcionario, author=request.user)
        curriculo, _ = Curriculo.objects.get_or_create(user=request.user)
    except Exception as e:
        messages.error(request, "Erro ao carregar os dados do currículo.")
        return redirect('authors:dashboard')

    # Formulários
    form = CurriculoForm(request.POST or None, request.FILES or None, instance=curriculo)
    formacao_formset = FormacaoFormSet(request.POST or None, instance=curriculo, prefix='formacao')
    curso_formset = CursoFormSet(request.POST or None, instance=curriculo, prefix='curso')
    competencias_formset = CompetenciasFormSet(request.POST or None, instance=curriculo, prefix='competencias')
    habilidades_formset = HabilidadesFormSet(request.POST or None, instance=curriculo, prefix='habilidades')
    mobilidade_formset = MobilidadeFormSet(request.POST or None, instance=curriculo, prefix='mobilidade')



    aba_atual = request.POST.get('aba_atual', 'geral')
    print(aba_atual,1)
    print(mobilidade_formset)
    if request.method == "POST":
        try:
            with transaction.atomic():
                if aba_atual == 'geral' and form.is_valid():
                    curriculo = form.save(commit=False)
                    curriculo.user = request.user
                    curriculo.save()

                    idioma_ids = request.POST.getlist('idiomas')
                    curriculo.idiomas.set(idioma_ids)
                    messages.success(request, "Dados gerais salvos com sucesso!")

                elif aba_atual == 'formacao' and formacao_formset.is_valid():
                    formacao_formset.instance = curriculo
                    formacao_formset.save()
                    messages.success(request, "Formações salvas com sucesso!")

                elif aba_atual == 'curso' and curso_formset.is_valid():
                    curso_formset.instance = curriculo
                    curso_formset.save()
                    messages.success(request, "Cursos salvos com sucesso!")

                elif aba_atual == 'competencias' and competencias_formset.is_valid():
                    competencias_formset.instance = curriculo
                    competencias_formset.save()
                    messages.success(request, "Competências salvas com sucesso!")

                elif aba_atual == 'habilidades' and habilidades_formset.is_valid():
                    habilidades_formset.instance = curriculo
                    habilidades_formset.save()
                    messages.success(request, "Habilidades salvas com sucesso!")

                if aba_atual == 'mobilidade' and mobilidade_formset.is_valid():
                    print("mob")
                    # Filtrar apenas formulários preenchidos
                    for form in mobilidade_formset:
                        if not form.cleaned_data.get('disponibilidade') and not form.cleaned_data.get('area_interesse'):
                            form.cleaned_data['DELETE'] = True  # marca para deletar
                    
                    mobilidade_formset.instance = curriculo
                    mobilidade_formset.save()
                    messages.success(request, "Mobilidade salva com sucesso!")
                    
                elif aba_atual == 'ficheiro' and form.is_valid():
                    print(aba_atual)
                    curriculo = form.save(commit=False)
                    curriculo.user = request.user
                    if 'ficheiro_cv' in request.FILES:
                        curriculo.ficheiro_cv = request.FILES['ficheiro_cv']
                    
                    if request.POST.get('remover_cv'):
                        if curriculo.ficheiro_cv:
                            curriculo.ficheiro_cv.delete(save=False)  # Deleta arquivo do storage
                            curriculo.ficheiro_cv = None

                    curriculo.save()
                    messages.success(request, "CV enviado/atualizado com sucesso!")

                else:
                    print("===== ERROS DE FORMSETS =====")
                    print("Form Geral Errors:", form.errors)
                    print("Formacao Errors:", formacao_formset.errors)
                    print("Curso Errors:", curso_formset.errors)
                    print("Competencias Errors:", competencias_formset.errors)
                    print("Habilidades Errors:", habilidades_formset.errors)
                    print("Mobilidade Errors:", mobilidade_formset.errors)
                    print("Formset non_form_errors:")
                    print("Formacao non_form_errors:", formacao_formset.non_form_errors())
                    print("Curso non_form_errors:", curso_formset.non_form_errors())
                    print("Competencias non_form_errors:", competencias_formset.non_form_errors())
                    print("Habilidades non_form_errors:", habilidades_formset.non_form_errors())
                    print("Mobilidade non_form_errors:", mobilidade_formset.non_form_errors())
                    messages.error(request, "Existem erros nos campos desta aba. Verifique e tente novamente.")

                return redirect('rhumanos:cadastrar_curriculo')

        except Exception as e:
            messages.error(request, f"Erro ao salvar os dados: {e}")

    # GET
    idiomas = Idioma.objects.all()
    selected_idiomas = curriculo.idiomas.values_list('id', flat=True)

    context = {
        'form': form,
        'formsets': {
            'formacoes': formacao_formset,
            'cursos': curso_formset,
            'competencias': competencias_formset,
            'habilidades': habilidades_formset,
            'mobilidade': mobilidade_formset,
        },
        'idiomas': idiomas,
        'selected_idiomas': selected_idiomas,
        'funcionario': funcionario,
    }
    return render(request, 'rhumanos/cadastrar_curriculo.html', context)

@login_required(login_url='authors:login', redirect_field_name='next')
def listar_curriculos(request: HttpRequest) -> HttpResponse:
    """
    Exibe uma listagem profissional de todos os currículos registados no sistema.

    Inclui:
    - Pesquisa por nome, cargo ou áreas de interesse
    - Filtros por regime de contrato e idioma
    - Paginação
    - Contexto de utilizador autenticado (funcionário)
    """

    # --- 1️⃣ Validação do utilizador autenticado ---
    funcionario = Funcionario.objects.select_related('departamento').filter(author=request.user).first()
    if not funcionario:
        logger.warning("Funcionário não encontrado para o utilizador %s", request.user.username)
        raise Http404("Funcionário não encontrado")

    curriculo_user = Curriculo.objects.select_related('user').filter(user=request.user).first()
    if not curriculo_user:
        logger.warning("Currículo não encontrado para o utilizador %s", request.user.username)
        raise Http404("Currículo do utilizador não encontrado")

    # --- 2️⃣ Queryset base optimizado ---
    curriculos = (
        Curriculo.objects
        .select_related('user')
        .prefetch_related(
            'idiomas',
            Prefetch('formacoes', queryset=FormacaoAcademica.objects.order_by('-ano_conclusao')),
            Prefetch('cursos_certificacoes', queryset=CursoCertificacao.objects.order_by('-ano_conclusao')),
        )
        .all()
    )

    # --- 3️⃣ Filtros e Pesquisa ---
    query = request.GET.get('q', '').strip()
    regime = request.GET.get('regime', '').strip()
    idioma_id = request.GET.get('idioma', '').strip()

    # 🔍 Pesquisa textual avançada
    if query:
        curriculos = curriculos.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(cargo_actual__icontains=query) |
            Q(areas_interesse__icontains=query)
        )
        logger.debug("Pesquisa aplicada: %s", query)

    # 🧩 Filtro por regime
    if regime:
        curriculos = curriculos.filter(regime_contrato=regime)
        logger.debug("Filtro por regime: %s", regime)

    # 🌐 Filtro por idioma
    if idioma_id:
        try:
            idioma = Idioma.objects.get(id=idioma_id)
            curriculos = curriculos.filter(idiomas=idioma)
            logger.debug("Filtro por idioma: %s", idioma)
        except Idioma.DoesNotExist:
            logger.warning("Idioma com ID %s não encontrado", idioma_id)
            curriculos = curriculos.none()

    # 🔢 Ordenação padrão
    curriculos = curriculos.distinct().order_by('user__first_name')

    # --- 4️⃣ Paginação ---
    page_obj, pagination_range = make_pagination(request, curriculos, PER_PAGE)

    # --- 5️⃣ Dados auxiliares ---
    idiomas = Idioma.objects.all().order_by('nome')
    regimes = Curriculo.REGIME_CONTRATO_CHOICES

    # --- 6️⃣ Contexto para o template ---
    context = {
        'titulo_pagina': 'Lista de Currículos',
        'funcionario': funcionario,
        'curriculos': page_obj,
        'pagination_range': pagination_range,
        'curriculo_user': curriculo_user,
        'idiomas': idiomas,
        'regimes': regimes,
        'query': query,
        'regime_selecionado': regime,
        'idioma_selecionado': idioma_id,
        'total_registros': curriculos.count(),
    }

    logger.info("Listagem de currículos gerada com sucesso por %s", request.user.username)
    return render(request, 'rhumanos/listar_curriculos.html', context)


@login_required(login_url='authors:login', redirect_field_name='next')
def detalhes_curriculo(request, id):
    """
    Exibe os detalhes completos de um currículo, incluindo:
    - Dados pessoais e profissionais
    - Formação Académica
    - Cursos e Certificações
    - Competências Digitais
    - Habilidades e Talentos
    - Mobilidade Interna
    """
    funcionario = Funcionario.objects.select_related('departamento').filter(author=request.user).first()
    if not funcionario:
        logger.warning("Funcionário não encontrado para o utilizador %s", request.user.username)
        raise Http404("Funcionário não encontrado")

    # --- Busca o currículo com todas as relações associadas ---
    curriculo = (
        Curriculo.objects
        .select_related('user')
        .prefetch_related(
            'idiomas',
            Prefetch('formacoes', queryset=FormacaoAcademica.objects.order_by('-ano_conclusao')),
            Prefetch('cursos_certificacoes', queryset=CursoCertificacao.objects.order_by('-ano_conclusao')),
            'competencias_digitais',
            'habilidades_talentos',
            'mobilidade_interna'
        )
        .filter(id=id)
        .first()
    )

    if not curriculo:
        raise Http404("Currículo não encontrado.")

    # --- Secções relacionadas ---
    formacoes = curriculo.formacoes.all()
    cursos = curriculo.cursos_certificacoes.all()
    competencias = curriculo.competencias_digitais.all()
    habilidades = curriculo.habilidades_talentos.all()
    mobilidades = curriculo.mobilidade_interna.all()

    # --- Contexto para o template ---
    context = {
        'titulo_pagina': f"Detalhes do Currículo - {curriculo.user.get_full_name() if curriculo.user else 'Usuário não definido'}",
        'curriculo': curriculo,
        'funcionario': funcionario,
        'formacoes': formacoes,
        'cursos': cursos,
        'competencias': competencias,
        'habilidades': habilidades,
        'mobilidades': mobilidades,
    }

    return render(request, 'rhumanos/detalhes_curriculo.html', context)

@login_required(login_url='login')  # Ajusta a URL de login
def curriculo_search(request):
    """
    View para pesquisar e filtrar currículos usando CurriculoFilter.
    """
    funcionario = Funcionario.objects.select_related('departamento').filter(author=request.user).first()
    if not funcionario:
        logger.warning("Funcionário não encontrado para o utilizador %s", request.user.username)
        raise Http404("Funcionário não encontrado")
    # Queryset inicial
    curriculos_queryset = Curriculo.objects.select_related('user').prefetch_related(
        'idiomas', 'formacoes', 'cursos_certificacoes', 'competencias_digitais', 
        'habilidades_talentos', 'mobilidade_interna'
    ).all()

    # Aplica filtros do GET
    curriculo_filter = CurriculoFilter(request.GET, queryset=curriculos_queryset)

    # Paginação
    paginator = Paginator(curriculo_filter.qs.distinct(), PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Contexto
    context = {
        'curriculos': page_obj,           # Currículos paginados
        'filter': curriculo_filter,       # Formulário de filtros
        'page_obj': page_obj,
        'funcionario': funcionario,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'query_string': request.META['QUERY_STRING'],
    }

    return render(request, 'rhumanos/curriculo_search.html', context)