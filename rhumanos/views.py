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
from expedient.models import Departamento
from .filters import CurriculoFilter

from django.db.models import F
from django.db.models import Value
from django.db.models.functions import Concat, Coalesce
# Create your views here.
# Configura um logger para registrar erros
logger = logging.getLogger(__name__)

PER_PAGE = 15

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



    aba_atual = request.POST.get('aba_atual', 'curriculo')
    print(aba_atual,1)
    # print(mobilidade_formset)
    if request.method == "POST":
        try:
            with transaction.atomic():
                #aba_atual = request.POST.get('aba_atual', 'geral')

                # --- Geral ---
                if aba_atual == 'curriculo' and form.is_valid():
                    print("teste")
                    curriculo = form.save(commit=False)
                    curriculo.user = request.user
                    curriculo.save()
                    idioma_ids = request.POST.getlist('idiomas')
                    curriculo.idiomas.set(idioma_ids)
                    messages.success(request, "Dados gerais salvos com sucesso!")

                # --- Formacao, Curso, Competencias, Habilidades (mantém o teu fluxo) ---
                elif aba_atual == 'formacao':
                    formacao_formset = FormacaoFormSet(request.POST, instance=curriculo, prefix='formacao')
                    if formacao_formset.is_valid():
                        formacao_formset.save()
                        messages.success(request, "Formações salvas com sucesso!")
                    else:
                        messages.error(request, "Erros nos campos de formação.")

                elif aba_atual == 'curso':
                    curso_formset = CursoFormSet(request.POST, instance=curriculo, prefix='curso')
                    if curso_formset.is_valid():
                        curso_formset.save()
                        messages.success(request, "Cursos salvos com sucesso!")
                    else:
                        messages.error(request, "Erros nos campos de cursos.")

                elif aba_atual == 'competencias':
                    competencias_formset = CompetenciasFormSet(request.POST, instance=curriculo, prefix='competencias')
                    if competencias_formset.is_valid():
                        competencias_formset.save()
                        messages.success(request, "Competências salvas com sucesso!")
                    else:
                        messages.error(request, "Erros nos campos de competências.")

                elif aba_atual == 'habilidades':
                    habilidades_formset = HabilidadesFormSet(request.POST, instance=curriculo, prefix='habilidades')
                    if habilidades_formset.is_valid():
                        habilidades_formset.save()
                        messages.success(request, "Habilidades salvas com sucesso!")
                    else:
                        messages.error(request, "Erros nos campos de habilidades.")

                # --- Mobilidade: PRUNE antes de validar ---
                elif aba_atual == 'mobilidade':
                    mobilidade_formset = MobilidadeFormSet(
                        request.POST or None,
                        request.FILES or None,
                        instance=curriculo,
                        prefix='mobilidade'
                    )

                    if mobilidade_formset.is_valid():
                        mobilidade_formset.save()
                        messages.success(request, "Mobilidade salva com sucesso!")
                    else:
                        # Debug detalhado
                        print("===== ERROS mobilidade_formset =====")
                        print(mobilidade_formset.errors)
                        print(mobilidade_formset.non_form_errors())
                        messages.error(request, "Erros nos campos de mobilidade. Verifique o formulário.")

                # --- Ficheiro (upload) ---
                elif aba_atual == 'ficheiro' and form.is_valid():
                    curriculo = form.save(commit=False)
                    curriculo.user = request.user
                    if 'ficheiro_cv' in request.FILES:
                        curriculo.ficheiro_cv = request.FILES['ficheiro_cv']

                    if request.POST.get('remover_cv') and curriculo.ficheiro_cv:
                        curriculo.ficheiro_cv.delete(save=False)
                        curriculo.ficheiro_cv = None

                    curriculo.save()
                    messages.success(request, "CV enviado/atualizado com sucesso!")

                else:
                    # se chegou aqui é porque a aba selecionada não passou validação
                    # imprime debug dos erros
                    print("===== ERROS DE FORMSETS (fallback) =====")
                    print("Form Geral Errors:", form.errors)
                    # Opcional: imprimir erros dos outros formsets (os que estão na memória)
                    print("Formacao Errors:", formacao_formset.errors)
                    print("Curso Errors:", curso_formset.errors)
                    print("Competencias Errors:", competencias_formset.errors)
                    print("Habilidades Errors:", habilidades_formset.errors)
                    print("Mobilidade Errors:", mobilidade_formset.errors)
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

    # curriculo_user = Curriculo.objects.select_related('user').filter(user=request.user).first()
    # if not curriculo_user:
    #     logger.warning("Currículo não encontrado para o utilizador %s", request.user.username)
    #     raise Http404("Currículo do utilizador não encontrado")

    # Verifica se um departamento foi selecionado na consulta GET
    departamento_id = request.GET.get('departamento')
    # print(departamento_id)
    # if departamento_id:
    #     try:
    #         # Filtra as atividades do departamento selecionado
    #         departamento = Departamento.objects.get(id=departamento_id)
    #         print(departamento)
    #         curriculos = curriculos.filter(user__funcionario__departamento_id=departamento_id)
    #         print(curriculos)
    #     except Departamento.DoesNotExist:
    #         # Caso o departamento não exista, podemos lançar um erro ou apenas não filtrar
    #         atividades = atividades.none()  # Isso pode ser alterado para um tratamento de erro personalizado
    
    # Obtém todos os departamentos para o filtro no formulário
    # departamentos = Departamento.objects.all().order_by('nome')
    
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
    departamento_id = request.GET.get('departamento')

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

    if departamento_id:
        try:
            departamento = Departamento.objects.get(id=departamento_id)
            print(departamento)
            curriculos = curriculos.filter(user__funcionario__departamento_id=departamento_id)
        except Departamento.DoesNotExist:
            curriculos = curriculos.none()
        
    departamentos = Departamento.objects.all().order_by('nome')
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
        'departamentos': departamentos,
        'departamento_selecionado': departamento_id,
        'curriculos': page_obj,
        'pagination_range': pagination_range,
        # 'curriculo_user': curriculo_user,
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

    # Remove o parâmetro page da query string
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    query_string = query_params.urlencode() 
    # Contexto
    context = {
        'curriculos': page_obj,           # Currículos paginados
        'filter': curriculo_filter,       # Formulário de filtros
        'page_obj': page_obj,
        'funcionario': funcionario,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'query_string': query_string,
    }

    return render(request, 'rhumanos/curriculo_search.html', context)






# from django.http import JsonResponse
# from django.contrib.auth import get_user_model
# from faker import Faker
# import random

# from rhumanos.models import Curriculo, Idioma
# #from funcionarios.models import Funcionario, Departamento

# def seed_curriculos_view(request):
#     fake = Faker('pt_PT')
#     User = get_user_model()
#     TOTAL = 40

#     # --- Criar departamentos se não existirem ---
#     departamentos = []
#     for nome in ["Recursos Humanos", "Tecnologia", "Finanças", "Jurídico", "Comercial"]:
#         dep, _ = Departamento.objects.get_or_create(nome=nome)
#         departamentos.append(dep)

#     # --- Criar idiomas se não existirem ---
#     idiomas = list(Idioma.objects.all())
#     if not idiomas:
#         idiomas = [
#             Idioma.objects.create(nome="Português"),
#             Idioma.objects.create(nome="Inglês"),
#             Idioma.objects.create(nome="Francês"),
#         ]

#     criados = 0
#     for _ in range(TOTAL):
#         nome = fake.name()
#         email = fake.unique.email()
#         telefone = fake.phone_number()
#         dep = random.choice(departamentos)

#         # Cria o usuário
#         user, created_user = User.objects.get_or_create(
#             username=email,
#             defaults={
#                 "first_name": nome.split()[0],
#                 "last_name": " ".join(nome.split()[1:]),
#                 "email": email,
#             }
#         )

#         # Cria funcionário
#         Funcionario.objects.get_or_create(
#             author=user,
#             defaults={
#                 "nome_completo": nome,
#                 "numero_telefone": telefone,
#                 "estado": "Ativo",
#                 "departamento": dep,
#             },
#         )

#         # Cria currículo
#         curriculo, created_cv = Curriculo.objects.get_or_create(
#             user=user,
#             defaults={
#                 "cargo_actual": fake.job(),
#                 "naturalidade": fake.city(),
#                 "contacto_telefonico": telefone,
#                 "endereco_electronico": email,
#                 "endereco_fisico": fake.address(),
#                 "areas_interesse": fake.sentence(),
#                 "regime_contrato": random.choice([r[0] for r in Curriculo.REGIME_CONTRATO_CHOICES]),
#                 "data_nascimento": fake.date_of_birth(minimum_age=22, maximum_age=55),
#             }
#         )

#         # Associa idiomas aleatórios
#         curriculo.idiomas.set(random.sample(idiomas, random.randint(1, len(idiomas))))

#         criados += 1

#     return JsonResponse({"message": f"{criados} currículos criados com sucesso!"})
