from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Autorizacao, Funcionario
from .forms.autorizacao_form import AutorizacaoForm
from django.http import Http404
from django.utils import timezone
from utils.expedient.pagination import make_pagination

import os

# PER_PAGE = int(os.environ.get('PER_PAGE', 10))
PER_PAGE = 8
@login_required(login_url='authors:login', redirect_field_name='next')
def cadastrar_autorizacao(request):
    funcionario = Funcionario.objects.filter(author=request.user).first()
    
    if not funcionario:
        raise Http404("Funcionário não encontrado")

    form = AutorizacaoForm(data=request.POST or None)

    if form.is_valid():
        autorizacao = form.save(commit=False)
        autorizacao.responsavel = funcionario  # Define o responsável como o funcionário logado
        autorizacao.data_autorizacao = timezone.now()  # Define a data de autorização
        autorizacao.save()

        # Se necessário, você pode adicionar lógica para enviar e-mails aqui

        messages.success(request, 'Autorização cadastrada com sucesso!')
        return redirect(reverse('autorizacao:listar_autorizacoes'))  # Redireciona para a lista de autorizações ou outra página desejada

    return render(request, 'autorizacao/cadastrar_autorizacao.html', {
        'form': form,
        'funcionario': funcionario,
        'form_action': reverse('autorizacao:cadastrar_autorizacao')
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def listar_autorizacoes(request):
    funcionario = Funcionario.objects.select_related('departamento').filter(author=request.user).first()
    
    if not funcionario:
        raise Http404("Funcionário não encontrado")
    
    autorizacoes = Autorizacao.objects.all()  # Obtém todas as autorizações
    
    # Paginação
   
    page_obj, pagination_range = make_pagination(request, autorizacoes, PER_PAGE)
    
    return render(request, 'autorizacao/listar_autorizacao.html', {
        'autorizacoes': page_obj,
        'funcionario': funcionario,
        'pagination_range': pagination_range,
    })
    
    
@login_required(login_url='authors:login', redirect_field_name='next')
def detalhes_autorizacao(request, id):
    # Obtendo a autorização com o ID fornecido ou retornando um erro 404 se não for encontrada
    autorizacao = get_object_or_404(Autorizacao, id=id)
    
    # Obtendo o funcionário associado ao usuário logado
    funcionario = Funcionario.objects.filter(author=request.user).first()
    if not funcionario:
        raise Http404("Funcionário não encontrado")

    return render(request, 'autorizacao/detalhes_autorizacao.html', {
        'autorizacao': autorizacao,
        'funcionario': funcionario,
    })