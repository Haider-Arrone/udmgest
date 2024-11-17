from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from .models import Atividade, Funcionario, TipoAtividade
from django.db.models.functions import TruncMonth
from actividades.forms.actividade_form import AtividadeForm  # Supondo que você tenha criado um formulário para Atividade
from utils.expedient.pagination import make_pagination
from .filters import ActivityFilter
from expedient.models import Departamento
PER_PAGE = 8
@login_required(login_url='authors:login', redirect_field_name='next')
def cadastrar_actividade(request):
    funcionario = Funcionario.objects.filter(author=request.user).first()
    
    if not funcionario:
        raise Http404("Funcionário não encontrado")

    tipos_atividade = TipoAtividade.objects.filter(departamento=funcionario.departamento)

    if request.method == "POST":
        form = AtividadeForm(data=request.POST)
    else:
        form = AtividadeForm()
        form.fields['tipo_atividade'].queryset = tipos_atividade  # Aplica o filtro de tipo de atividade

    if form.is_valid():
        atividade = form.save(commit=False)
        atividade.funcionario = funcionario  # Define o funcionário logado como responsável
        atividade.data = timezone.now()  # Define a data de criação da atividade
        atividade.save()


        messages.success(request, 'Atividade cadastrada com sucesso!')
        return redirect(reverse('actividades:listar_actividades'))  # Redireciona para a lista de atividades ou outra página desejada

    return render(request, 'actividades/cadastrar_actividade.html', {
        'form': form,
        'funcionario': funcionario,
        'form_action': reverse('actividades:cadastrar_actividade')
    })
    

@login_required(login_url='authors:login', redirect_field_name='next')
def listar_actividades(request):
    funcionario = Funcionario.objects.select_related('departamento').filter(author=request.user).first()
    
    if not funcionario:
        raise Http404("Funcionário não encontrado")
    
    # Obtém todas as atividades associadas ao funcionário
    atividades = Atividade.objects.filter(funcionario=funcionario)  # Ajuste conforme necessário
    
    departamento_id = request.GET.get('departamento')
    if departamento_id:
        atividades = atividades.filter(funcionario__departamento_id=departamento_id)


    
    departamentos = Departamento.objects.all()
    # Paginação
    page_obj, pagination_range = make_pagination(request, atividades, PER_PAGE)
    
    return render(request, 'actividades/listar_actividade.html', {  # Altere o caminho do template conforme necessário
        'actividades': page_obj,
        'funcionario': funcionario,
        'pagination_range': pagination_range,
        'departamentos': departamentos,  # Passa os departamentos para o template
        'departamento_selecionado': departamento_id, 
    })
    
    
@login_required(login_url='authors:login', redirect_field_name='next')
def detalhes_actividade(request, id):
    # Obtendo a atividade com o campo apropriado ou retornando um erro 404 se não for encontrada
    atividade = get_object_or_404(Atividade, pk=id)  # Ajuste 'pk' conforme necessário

    # Obtendo o funcionário associado ao usuário logado
    funcionario = Funcionario.objects.filter(author=request.user).first()
    if not funcionario:
        raise Http404("Funcionário não encontrado")

    return render(request, 'actividades/detalhes_actividade.html', {
        'actividade': atividade,
        'funcionario': funcionario,
    })
 
@login_required(login_url='authors:login', redirect_field_name='next')   
def relatorio_actividades(request):
    # Obter a lista de departamentos para o filtro
    departamentos = Departamento.objects.all()

    # Pegar o departamento do GET, se existir
    departamento_id = request.GET.get('departamento')
    
    funcionario = Funcionario.objects.filter(author=request.user).first()
    
    if not funcionario:
        raise Http404("Funcionário não encontrado")
    
    # Filtrar atividades por departamento se um departamento for selecionado
    if departamento_id:
         atividades = Atividade.objects.filter(funcionario__departamento_id=departamento_id)
    else:
        atividades = Atividade.objects.all()

    # Coletar dados de atividades agrupados por status
    status_data = atividades.values('status').annotate(total=Count('id'))

    # Coletar dados de atividades agrupados por tipo
    tipo_data = atividades.values('tipo_atividade').annotate(total=Count('id'))

    # Coletar dados de atividades por funcionário
    funcionario_data = atividades.values('funcionario__nome_completo').annotate(total=Count('id'))

    # Coletar dados de tempo gasto por funcionário
    tempo_gasto_data = atividades.values('funcionario__nome_completo').annotate(total_tempo=Sum('tempo_gasto'))
    tempo_gasto_totals = [item['total_tempo'].total_seconds() / 3600 for item in tempo_gasto_data]  # Convertendo para horas


    # Coletar dados de atividades concluídas e atrasadas
    status_concluidas_data = atividades.filter(status='concluida').count()
    status_atrasadas_data = atividades.filter(status='atrasada').count()

    # Coletar dados de dificuldade das atividades
    dificuldade_data = atividades.values('dificuldade').annotate(total=Count('id'))
    
    # Coletar dados de prioridade das atividades
    prioridade_data = atividades.values('prioridade').annotate(total=Count('id'))

    # Coletar dados de atividades por mês
    atividades_por_mes = atividades.annotate(month=TruncMonth('data')).values('month').annotate(total=Count('id')).order_by('month')

    # Preparar os dados para os gráficos
    contexto = {
        'departamentos': departamentos,
        'departamento_selecionado': departamento_id, 
        'selected_departamento': departamento_id,
        'status_labels': [item['status'] for item in status_data],
        'status_totals': [item['total'] for item in status_data],
        'tipo_labels': [item['tipo_atividade'] for item in tipo_data],
        'tipo_totals': [item['total'] for item in tipo_data],
        'funcionario_labels': [item['funcionario__nome_completo'] for item in funcionario_data],
        'funcionario_totals': [item['total'] for item in funcionario_data],
        'tempo_gasto_labels': [item['funcionario__nome_completo'] for item in tempo_gasto_data],
        'tempo_gasto_totals': tempo_gasto_totals,  # Usar a lista convertida
        'status_concluidas': status_concluidas_data,
        'status_atrasadas': status_atrasadas_data,
        'dificuldade_labels': [item['dificuldade'] for item in dificuldade_data],
        'dificuldade_totals': [item['total'] for item in dificuldade_data],
        'prioridade_labels': [item['prioridade'] for item in prioridade_data],
        'prioridade_totals': [item['total'] for item in prioridade_data],
        'mes_labels': [item['month'].strftime('%Y-%m') for item in atividades_por_mes],
        'mes_totals': [item['total'] for item in atividades_por_mes],
        'funcionario': funcionario,
    }

    return render(request, 'actividades/relatorio_actividades.html', contexto)

@login_required(login_url='authors:login', redirect_field_name='next')
def actividade_search(request):
    id_departamento = Funcionario.objects.filter(author=request.user).first()
    if not id_departamento:
        raise Http404()

    departamentos = Departamento.objects.all()
    

    
    actividades = ActivityFilter(request.GET, queryset=Atividade.objects.all())
    # filtro = ActivityFilter(request.GET, queryset=Atividade.objects.all())
    
    # if request.GET.get('departamento'):
    #     departamento_id = request.GET['departamento']
    #     atividades_queryset = atividades_queryset.filter(funcionario__departamento_id=departamento_id)
    atividades_queryset = Atividade.objects.all()

    # Aplica o filtro de departamento, se houver
    departamento_selecionado = request.GET.get('departamento', '')
    if departamento_selecionado:
        atividades_queryset = atividades_queryset.filter(funcionario__departamento_id=departamento_selecionado)


    # Aplica o ActivityFilter à queryset filtrada
    atividades = ActivityFilter(request.GET, queryset=atividades_queryset)


    # page_obj, pagination_context = make_pagination(request, filtro.qs, PER_PAGE)
    page_obj, pagination_context = make_pagination(request, atividades.qs, PER_PAGE)

    print(f"Current page: {pagination_context['current_page']}")
    print(f"Total pages: {pagination_context['total_pages']}")
    print(f"Pagination range: {pagination_context['pagination_range']}")
    print(f"Query string: {pagination_context['query_string']}")

    return render(request, 'actividades/actividade_search.html', {
        'filtros': page_obj,
        'pagination_range': pagination_context['pagination_range'],
        'funcionario': id_departamento,
        'actividades': actividades,
        'departamentos': departamentos, 
        'departamento_selecionado': departamento_selecionado, 
        'query_string': pagination_context['query_string'],
        'first_page_out_of_range': pagination_context['first_page_out_of_range'],
        'last_page_out_of_range': pagination_context['last_page_out_of_range'],
        'current_page': pagination_context['current_page'],
        'total_pages': pagination_context['total_pages'],
    })