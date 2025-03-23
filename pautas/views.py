from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from expedient.models import  Funcionario, Departamento
from django.db.models.functions import TruncMonth
from actividades.forms.actividade_form import AtividadeForm  # Supondo que você tenha criado um formulário para Atividade
from utils.expedient.pagination import make_pagination
from .filters import PautaFilter
from .models import Semestre, Pauta, Curso, Disciplina, Faculdade
from django.http import JsonResponse, HttpResponse
from .forms.pauta_form import PautaForm

# Defina o número de itens por página
PER_PAGE = 10

def get_cursos(request, faculdade_id):
    cursos = Curso.objects.filter(faculdade_id=faculdade_id).values('id', 'nome')
    print(cursos)
    return JsonResponse({'cursos': list(cursos)})

def get_disciplinas(request, curso_id):
    # Obtém as disciplinas para o curso selecionado
    disciplinas = Disciplina.objects.filter(curso_id=curso_id)
    
    # Cria uma lista de dicionários contendo as id e nome das disciplinas
    disciplinas_list = [{'id': disciplina.id, 'nome': disciplina.nome} for disciplina in disciplinas]
    
    return JsonResponse({'disciplinas': disciplinas_list})

@login_required(login_url='authors:login', redirect_field_name='next')
def pauta_search(request):
    try:
        # Obtenha o id do departamento (ajuste conforme necessário)
        id_departamento = Funcionario.objects.filter(author=request.user).first()
        if not id_departamento:
            raise Http404("Departamento não encontrado")

        # Pegue as disciplinas e semestres para usá-los como filtros
        disciplinas = Disciplina.objects.all()
        semestres = Semestre.objects.all()

        # Crie um filtro para as pautas
        pautas_queryset = Pauta.objects.filter(ativo=True)

        # Obtém os parâmetros de filtro da URL
        faculdade_id = request.GET.get('faculdade')
        curso_id = request.GET.get('curso')
        disciplina_id = request.GET.get('disciplina')
        semestre_id = request.GET.get('semestre')
        turma = request.GET.get('turma')
        docente = request.GET.get('docente')

        if faculdade_id:
            pautas_queryset = pautas_queryset.filter(faculdade_id=faculdade_id)

        # Filtra as pautas com base no curso, se fornecido
        if curso_id:
            pautas_queryset = pautas_queryset.filter(curso_id=curso_id)

        # Filtra as pautas com base na disciplina, se fornecida
        if disciplina_id:
            pautas_queryset = pautas_queryset.filter(disciplina_id=disciplina_id)


        # Filtra as pautas com base no semestre, se fornecido
        if semestre_id:
            pautas_queryset = pautas_queryset.filter(semestre_id=semestre_id)

        # Filtra as pautas com base na turma, se fornecida
        if turma:
            pautas_queryset = pautas_queryset.filter(turma__icontains=turma)
        if docente:
            pautas_queryset = pautas_queryset.filter(docente__icontains=docente)
        

        # Aplica o filtro de pauta
        pautas = PautaFilter(request.GET, queryset=pautas_queryset)

        # Criação da paginação
        page_obj, pagination_context = make_pagination(request, pautas.qs, PER_PAGE)

        # Retorna a resposta renderizada
        return render(request, 'pautas/pauta_search.html', {
            'filtros': page_obj,
            'pagination_range': pagination_context['pagination_range'],
            'funcionario': id_departamento,
            'pautas': pautas,
            'disciplinas': disciplinas,
            'semestres': semestres,
            'query_string': pagination_context['query_string'],
            'first_page_out_of_range': pagination_context['first_page_out_of_range'],
            'last_page_out_of_range': pagination_context['last_page_out_of_range'],
            'current_page': pagination_context['current_page'],
            'total_pages': pagination_context['total_pages'],
        })

    except Funcionario.DoesNotExist:
        # Erro específico se o Funcionario não for encontrado
        return HttpResponse("Funcionário não encontrado.", status=404)
    except Pauta.DoesNotExist:
        # Erro específico se não houver Pautas
        return HttpResponse("Pautas não encontradas.", status=404)
    except Exception as e:
        # Captura qualquer outro erro inesperado
        return HttpResponse(f"Ocorreu um erro inesperado: {str(e)}", status=500)

@login_required(login_url='authors:login', redirect_field_name='next')
def detalhes_pauta(request, id):
    # Obtendo a atividade com o campo apropriado ou retornando um erro 404 se não for encontrada
    pauta = get_object_or_404(Pauta, pk=id)  # Ajuste 'pk' conforme necessário

    # Obtendo o funcionário associado ao usuário logado
    funcionario = Funcionario.objects.filter(author=request.user).first()
    if not funcionario:
        raise Http404("Funcionário não encontrado")

    return render(request, 'pautas/detalhes_pauta.html', {
        'pauta': pauta,
        'funcionario': funcionario,
    })
    
@login_required(login_url='authors:login', redirect_field_name='next')
def cadastrar_pauta(request):
    funcionario = Funcionario.objects.filter(author=request.user).first()
    
    if not funcionario:
        raise Http404("Funcionário não encontrado")

    
    if request.method == "POST":
        form = PautaForm(data=request.POST, files=request.FILES) 
        
        if form.is_valid():
            if form.is_valid():
                pauta = form.save(commit=False)
                pauta.criado_por = request.user  # Definir o usuário autenticado como criador
                pauta.ativo= True
                pauta.save()
                
                messages.success(request, 'Pauta cadastrada com sucesso!')
                return redirect(reverse('pautas:pauta_search'))  # Redireciona para a lista de atividades ou outra página desejada

    else:
        form = PautaForm()

        
    return render(request, 'pautas/cadastrar_pauta.html', {
        'form': form,
        'funcionario': funcionario,
        'form_action': reverse('pautas:cadastrar_pauta')
    })
    
@login_required(login_url='authors:login', redirect_field_name='next')
def editar_pauta(request, pauta_id):
    # Obtém o funcionário relacionado ao usuário
    funcionario = Funcionario.objects.filter(author=request.user).first()
    if not funcionario:
        raise Http404("Funcionário não encontrado")

    # Obtém a pauta específica que será editada
    pauta = get_object_or_404(Pauta, id=pauta_id)

    # Verifica se o funcionário é o criador ou tem permissões para editar
    # if pauta.criado_por != request.user:
    #     raise Http404("Você não tem permissão para editar esta pauta")

    if request.method == "POST":
        form = PautaForm(data=request.POST, files=request.FILES, instance=pauta)  # Passa a instância para edição
        
        if form.is_valid():
            # Atualiza a pauta com os novos dados
            pauta = form.save(commit=False)
            pauta.modificado_por = request.user  # Define o usuário autenticado como responsável pela atualização
            pauta.data_modificacao = timezone.now()
            pauta.save()
            
            messages.success(request, 'Pauta atualizada com sucesso!')
            return redirect(reverse('pautas:pauta_search'))  # Redireciona para a lista de pautas

    else:
        form = PautaForm(instance=pauta)  # Preenche o formulário com os dados existentes da pauta

    return render(request, 'pautas/cadastrar_pauta.html', {
        'form': form,
        'funcionario': funcionario,
        'form_action': reverse('pautas:editar_pauta', args=[pauta.id]),
    })

@login_required(login_url='authors:login', redirect_field_name='next')
def apagar_pauta(request, pauta_id):
    funcionario = Funcionario.objects.filter(author=request.user).first()
    if not funcionario:
        raise Http404("Funcionário não encontrado")
    # Obtém a instância da Pauta, ou 404 se não encontrada
    pauta = get_object_or_404(Pauta, id=pauta_id)

    # Verifica se o usuário tem permissão para deletar a pauta (opcional)
    # if pauta.criado_por != request.user:
    #     messages.error(request, "Você não tem permissão para apagar esta pauta.")
    #     return redirect(reverse('pautas:pauta_search'))

    if request.method == "POST":
        # Deleta a pauta
        #pauta.delete()
        pauta.ativo = False
        pauta.modificado_por = request.user  # Define o usuário autenticado como responsável pela atualização
        pauta.data_modificacao = timezone.now()
        pauta.save()

        messages.success(request, 'Pauta apagada com sucesso!')
        return redirect(reverse('pautas:pauta_search'))  # Redireciona para a lista de pautas ou outra página desejada

    return render(request, 'pautas/confirmar_apagar_pauta.html', {
        'pauta': pauta,
        'funcionario': funcionario,
    })