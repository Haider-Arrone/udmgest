from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from .models import Atividade, Funcionario
from django.db.models.functions import TruncMonth
from actividades.forms.actividade_form import AtividadeForm  # Supondo que você tenha criado um formulário para Atividade
from utils.expedient.pagination import make_pagination
from .filters import ActivityFilter

PER_PAGE = 8
@login_required(login_url='authors:login', redirect_field_name='next')
def cadastrar_actividade(request):
    funcionario = Funcionario.objects.filter(author=request.user).first()
    
    if not funcionario:
        raise Http404("Funcionário não encontrado")

    form = AtividadeForm(data=request.POST or None)

    if form.is_valid():
        atividade = form.save(commit=False)
        atividade.funcionario = funcionario  # Define o funcionário como o responsável logado
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

    # Paginação
    page_obj, pagination_range = make_pagination(request, atividades, PER_PAGE)
    
    return render(request, 'actividades/listar_actividade.html', {  # Altere o caminho do template conforme necessário
        'actividades': page_obj,
        'funcionario': funcionario,
        'pagination_range': pagination_range,
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
    
def relatorio_actividades(request):
    # Coletar dados de atividades agrupados por status
    status_data = Atividade.objects.values('status').annotate(total=Count('id'))

    # Coletar dados de atividades agrupados por tipo
    tipo_data = Atividade.objects.values('tipo_atividade').annotate(total=Count('id'))

    # Coletar dados de atividades por funcionário
    funcionario_data = Atividade.objects.values('funcionario__nome_completo').annotate(total=Count('id'))

    # Coletar dados de tempo gasto por funcionário
    tempo_gasto_data = Atividade.objects.values('funcionario__nome_completo').annotate(total_tempo=Sum('tempo_gasto'))

    # Coletar dados de atividades concluídas e atrasadas
    status_concluidas_data = Atividade.objects.filter(status='concluida').count()
    status_atrasadas_data = Atividade.objects.filter(status='atrasada').count()

    # Coletar dados de dificuldade das atividades
    dificuldade_data = Atividade.objects.values('dificuldade').annotate(total=Count('id'))
    print(dificuldade_data)
    # Coletar dados de prioridade das atividades
    prioridade_data = Atividade.objects.values('prioridade').annotate(total=Count('id'))
    print(prioridade_data)
    # Coletar dados de atividades por mês
    atividades_por_mes = Atividade.objects.annotate(month=TruncMonth('data')).values('month').annotate(total=Count('id')).order_by('month')

    # Preparar os dados para os gráficos
    contexto = {
        'status_labels': [item['status'] for item in status_data],
        'status_totals': [item['total'] for item in status_data],
        'tipo_labels': [item['tipo_atividade'] for item in tipo_data],
        'tipo_totals': [item['total'] for item in tipo_data],
        'funcionario_labels': [item['funcionario__nome_completo'] for item in funcionario_data],
        'funcionario_totals': [item['total'] for item in funcionario_data],
        'tempo_gasto_labels': [item['funcionario__nome_completo'] for item in tempo_gasto_data],
        'tempo_gasto_totals': [item['total_tempo'] for item in tempo_gasto_data],
        'status_concluidas': status_concluidas_data,
        'status_atrasadas': status_atrasadas_data,
        'dificuldade_labels': [item['dificuldade'] for item in dificuldade_data],
        'dificuldade_totals': [item['total'] for item in dificuldade_data],
        'prioridade_labels': [item['prioridade'] for item in prioridade_data],
        'prioridade_totals': [item['total'] for item in prioridade_data],
        'mes_labels': [item['month'].strftime('%Y-%m') for item in atividades_por_mes],
        'mes_totals': [item['total'] for item in atividades_por_mes],
    }

    return render(request, 'actividades/relatorio_actividades.html', contexto)

@login_required(login_url='authors:login', redirect_field_name='next')
def actividade_search(request):
    id_departamento = Funcionario.objects.filter(author=request.user).first()
    if not id_departamento:
        raise Http404()

    actividades = ActivityFilter(request.GET, queryset=Atividade.objects.all())
    filtro = ActivityFilter(request.GET, queryset=Atividade.objects.all())

    page_obj, pagination_context = make_pagination(request, filtro.qs, PER_PAGE)

    print(f"Current page: {pagination_context['current_page']}")
    print(f"Total pages: {pagination_context['total_pages']}")
    print(f"Pagination range: {pagination_context['pagination_range']}")
    print(f"Query string: {pagination_context['query_string']}")

    return render(request, 'actividades/actividade_search.html', {
        'filtros': page_obj,
        'pagination_range': pagination_context['pagination_range'],
        'funcionario': id_departamento,
        'actividades': actividades,
        'query_string': pagination_context['query_string'],
        'first_page_out_of_range': pagination_context['first_page_out_of_range'],
        'last_page_out_of_range': pagination_context['last_page_out_of_range'],
        'current_page': pagination_context['current_page'],
        'total_pages': pagination_context['total_pages'],
    })