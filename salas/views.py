from django.shortcuts import render
import os
from django.db.models.functions import ExtractWeekDay
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from utils.expedient.pagination import make_pagination
from django.utils import timezone
import authors
from .models import Sala, Ocupacao
from authors.models import Profile
from collections import defaultdict
from django.contrib.auth.models import User
from .filters import Ocupacao_Filter
from expedient.models import Expedient, Funcionario, Parecer
from django.shortcuts import render
import matplotlib.pyplot as plt
import numpy as np
from django.db.models import Count
from .models import Sala, Ocupacao
from datetime import timedelta
from datetime import datetime, timedelta
# Create your views here.

@login_required(login_url='authors:login', redirect_field_name='next')
def consulta_sala(request):
    salas = Sala.objects.all()
    ocupacoes = Ocupacao.objects.all()

    print(ocupacoes)
    dados_grafico = []

    for ocupacao in ocupacoes:
        hora_inicio = datetime.strptime(str(ocupacao.hora_inicio), "%H:%M:%S").time()
        hora_fim = datetime.strptime(str(ocupacao.hora_fim), "%H:%M:%S").time()

        diferenca_minutos = (hora_fim.hour * 60 + hora_fim.minute) - (hora_inicio.hour * 60 + hora_inicio.minute)
        dados_grafico.append(diferenca_minutos)
    # Preparar dados para o template
    context = {
        'salas': salas,
        #'horas_do_dia': horas_do_dia,
        'ocupacoes': ocupacoes,
        'dados_grafico': dados_grafico
    }

    return render(request, 'salas/consulta.html', context)


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_salas_detail(request, id):
    sala = Sala.objects.filter(
        pk=id
    ).first()
    if not sala:
        raise Http404()

   # form = AuthorExpedientForm(data=request.POST or None,
    ##                           files=request.FILES or None,
       #                        instance=expedient)
   
    print(sala)
    #id_departamento = Funcionario.objects.filter(author=request.user).first()
    # print(id_departamento.departamento)

    ocupacoes = Ocupacao.objects.filter(sala=sala)
    print(ocupacoes)
    ocupacoes_por_dia = []
    dias_da_semana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']
    for dia in dias_da_semana:
        ocupacoes_do_dia = [ocupacao for ocupacao in ocupacoes if ocupacao.dia_semana == dia]
        ocupacoes_por_dia.append((dia, ocupacoes_do_dia))
        
    print(ocupacoes_por_dia)
    numeros = range(1, 15)

    #profile = Profile.objects.filter(author=usuario).first()
    funcionario = Funcionario.objects.filter(author=request.user).first()
    dias_da_semana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']
    #funcionario_expedient = Funcionario.objects.filter(author=usuario).first()
    return render(request,
                  'salas/sala-detail.html',
                  context={
                           'ocupacoes': ocupacoes, 'funcionario': funcionario,
                           'dias': dias_da_semana,
                           'ocupacoes_por_dia': ocupacoes_por_dia,
                           'numeros': numeros,
                           }
                  )
    

"""expedients = Expedient.objects.filter(estado='Respondido',
                                          usuario=request.user
                                          )[:5]
    funcionario = Funcionario.objects.filter(author=request.user).first()
    emitidos = Expedient.objects.filter(
        usuario=request.user
    ).exclude(estado='Respondido',)
    num_emit = Expedient.objects.filter(
        usuario=request.user
    ).exclude(estado='Respondido',).count()
    num_total = Expedient.objects.filter(
        usuario=request.user
    ).count()
    num_recebidos = Expedient.objects.filter(estado='Respondido',
                                             usuario=request.user
                                             ).count()
    print(num_total)
    print(num_emit)
    print(num_recebidos)
    dados = [num_emit, num_recebidos, num_total]
    dados_des = ['emitidos', 'recebidos', 'num_total']
    return render(request,
                  'authors/pages/dashbord.html',
                  {
                      'expedients': expedients,
                      'funcionario': funcionario,

                      'dados': dados,
                      'des': dados_des,
                  }
                  )
                  
"""
                  
@login_required(login_url='authors:login', redirect_field_name='next')
def salas_search(request):
    #search_term = request.GET.get('search', '').strip()
    #form = AuthorExpedientFormFilter(request.GET)

    id_departamento = Funcionario.objects.filter(author=request.user).first()
    if not id_departamento:
        raise Http404()
    #ver_funcionario = Funcionario.objects.filter(author=request.user).first()
    print(id_departamento.departamento.id)

    if id_departamento:
        ocupacaoes = Ocupacao_Filter(
            request.GET, queryset=Ocupacao.objects.all())
    else:
        raise Http404()

    # page_obj, pagination_range = make_pagination(
    # request, expedients, PER_PAGE)
    filtro = Ocupacao_Filter(request.GET, queryset=Ocupacao.objects.all())
    # recipes = recipes.filter(is_published=True)
    #recipe = Recipe.objects.filter(id=id, is_published=True).order_by('-id').first
    return render(request, 'salas/sala_search.html',
                  context={
                      # 'page_title': f'Search for "{search_term}"',
                      # 'search_term': search_term,
                       #'filtro': page_obj,
                       #'pagination_range': pagination_range,
                      # 'additional_url_query': f'&search={search_term}',
                      'funcionario': id_departamento,
                      'filtro': filtro,
                      # 'form': form,
                      'ocupacoes': ocupacaoes,

                  })

