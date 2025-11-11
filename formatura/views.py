from django.shortcuts import render, get_object_or_404
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Presenca, Formatura, PontoAgenda
from expedient.models import Funcionario, Departamento  # importa o modelo Funcionario
from datetime import datetime, date
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date, timedelta
import re
from simple_history.utils import update_change_reason
from django.db import transaction
from formatura.forms.formatura_form import FormaturaForm, PontoAgendaForm, PontoAgendaFormSet
from django.db.models import Prefetch, Q



# def is_admin(user):
#     return user.is_superuser  # Ou user.is_staff, se quiser incluir staff também


# Create your views here.

# @user_passes_test(is_admin, login_url='authors:login')
# def upload_presenca(request):
#     if not request.user.is_superuser:
#             messages.error(request, "Acesso negado: apenas administradores podem aceder a esta funcionalidade.")
#             return redirect('expedient:home')
#     funcionario = get_object_or_404(Funcionario, author=request.user) 
#     if request.method == "POST" and request.FILES.get('excel_file'):
#         excel_file = request.FILES['excel_file']

#         try:
            
#             # 📘 Lê o ficheiro Excel
#             df = pd.read_excel(excel_file, engine='openpyxl')

#             # 🔹 Remove linhas e colunas vazias
#             df = df.dropna(axis=0, how='all').dropna(axis=1, how='all')

#             # 🔹 Confirma colunas essenciais
#             colunas_esperadas = ['Employee ID', 'Name', 'Department']
#             for coluna in colunas_esperadas:
#                 if coluna not in df.columns:
#                     messages.error(request, f"Coluna '{coluna}' não encontrada no ficheiro.")
#                     return redirect('upload_presenca')

#             # 🔹 Detecta a coluna do dia (a única que varia)
#             dia_coluna = next((c for c in df.columns if c not in colunas_esperadas), None)
#             if not dia_coluna:
#                 messages.error(request, "Não foi encontrada a coluna correspondente ao dia do mês.")
#                 return redirect('upload_presenca')

#             registros_importados = 0
#             registros_ignorados = 0

#             # 🔁 Itera sobre as linhas do ficheiro
#             for index, row in df.iterrows():
#                 employee_id = row.get('Employee ID')
#                 hora_val = row.get(dia_coluna)

#                 if pd.isnull(employee_id) or pd.isnull(hora_val):
#                     registros_ignorados += 1
#                     continue

#                 # 🔹 Verifica se o usuário existe
#                 try:
#                     usuario = User.objects.get(pk=int(employee_id))
#                     funcionario_registro  = Funcionario.objects.get(author=usuario)
#                 except User.DoesNotExist:
#                     registros_ignorados += 1
#                     messages.warning(request, f"Usuário com ID {employee_id} não encontrado (linha {index + 2}).")
#                     continue
#                 except Funcionario.DoesNotExist:
#                     registros_ignorados += 1
#                     messages.warning(request, f"Funcionário para o usuário {employee_id} não encontrado (linha {index + 2}).")
#                     continue

#                 # 🕒 Processa a hora
#                 hora_entrada = None

#                 # Caso já seja datetime ou Timestamp (Excel interpreta como hora)
#                 if hasattr(hora_val, "time"):
#                     try:
#                         hora_entrada = hora_val.time()
#                     except Exception:
#                         hora_entrada = None

#                 # Caso seja string
#                 if hora_entrada is None:
#                     hora_str = str(hora_val).strip().replace("\n", " ").replace("\r", "")
#                     parsed = None
#                     formatos_possiveis = ("%H:%M", "%H:%M:%S", "%H.%M", "%I:%M %p", "%I:%M:%S %p")

#                     for fmt in formatos_possiveis:
#                         try:
#                             parsed = datetime.strptime(hora_str, fmt).time()
#                             break
#                         except Exception:
#                             continue

#                     # Fallback automático do pandas
#                     if parsed is None:
#                         try:
#                             ts = pd.to_datetime(hora_str, errors="coerce")
#                             if not pd.isnull(ts):
#                                 parsed = ts.time()
#                         except Exception:
#                             parsed = None

#                     if parsed is None:
#                         registros_ignorados += 1
#                         messages.warning(request, f"Hora inválida na linha {index + 2}: {hora_str}")
#                         continue

#                     hora_entrada = parsed

#                 # 🗓 Cria a data de presença com base no nome da coluna
#                 today = date.today()
#                 try:
#                     dia = int(str(dia_coluna).strip())
#                     data_presenca = date(today.year, today.month, dia)
#                 except ValueError:
#                     messages.error(request, f"Coluna '{dia_coluna}' não é um número válido de dia.")
#                     return redirect('upload_presenca')

#                 # 💾 Cria ou atualiza presença
#                 Presenca.objects.update_or_create(
#                     usuario=usuario,
#                     data_presenca=data_presenca,
#                     defaults={
#                         'hora_entrada': hora_entrada,
#                         'origem_registo': 'Importação Excel'
#                     }
#                 )
#                 registros_importados += 1

#             # ✅ Mensagens de sucesso/falha
#             messages.success(request, f"{registros_importados} registros importados com sucesso!")
#             if registros_ignorados:
#                 messages.warning(request, f"{registros_ignorados} registros foram ignorados por erro ou falta de dados.")

#             return redirect(reverse('formatura:upload_presenca'))

#         except Exception as e:
#             messages.error(request, f"Erro ao processar o ficheiro: {str(e)}")

#     return render(request, 'formatura/upload_presenca.html', {
#         'funcionario': funcionario,
#         'form_action': reverse('formatura:upload_presenca'),
#     })
   
@login_required(login_url='authors:login')
def upload_presenca(request):
    if not request.user.is_superuser:
        messages.error(request, "Acesso negado: apenas administradores podem aceder a esta funcionalidade.")
        return redirect('expedient:home')

    funcionario = get_object_or_404(Funcionario, author=request.user)

    if request.method == "POST" and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']

        try:
            df = pd.read_excel(excel_file, engine='openpyxl')
            df = df.dropna(axis=0, how='all').dropna(axis=1, how='all')

            # ✅ Colunas obrigatórias
            colunas_esperadas = ['Employee ID', 'Name', 'Department']
            for coluna in colunas_esperadas:
                if coluna not in df.columns:
                    messages.error(request, f"Coluna obrigatória '{coluna}' não encontrada.")
                    return redirect('formatura:upload_presenca')

            # ✅ Identificar a coluna de dia
            colunas_dias = [c for c in df.columns if c not in colunas_esperadas]
            if not colunas_dias:
                messages.error(request, "Nenhuma coluna de dia encontrada no ficheiro.")
                return redirect('formatura:upload_presenca')

            # Pegamos a primeira coluna (pois é um ficheiro de um só dia)
            dia_coluna = colunas_dias[0]

            # ✅ Tentar extrair o número do dia (ex: "16")
            try:
                dia = int(re.findall(r'\d+', str(dia_coluna))[0])
            except (IndexError, ValueError):
                messages.error(request, f"Nome da coluna de dia inválido: {dia_coluna}")
                return redirect('formatura:upload_presenca')

            # ✅ Permite definir data com base no nome do ficheiro (ex: presencas_2025-10-09.xlsx)
            match_data = re.search(r'(\d{4})[-_](\d{2})[-_](\d{2})', excel_file.name)
            if match_data:
                ano, mes, _ = map(int, match_data.groups())
            else:
                hoje = date.today()
                ano, mes = hoje.year, hoje.month

            data_presenca = date(ano, mes, dia)

            registros_importados = 0
            registros_ignorados = 0

            for index, row in df.iterrows():
                employee_id = row.get('Employee ID')
                hora_val = row.get(dia_coluna)

                if pd.isnull(employee_id) or pd.isnull(hora_val):
                    registros_ignorados += 1
                    continue

                try:
                    usuario = User.objects.get(pk=int(employee_id))
                except User.DoesNotExist:
                    registros_ignorados += 1
                    messages.warning(request, f"Usuário com ID {employee_id} não encontrado (linha {index + 2}).")
                    continue

                # 🕒 Processar hora
                hora_entrada = None
                if hasattr(hora_val, "time"):
                    hora_entrada = hora_val.time()
                else:
                    hora_str = str(hora_val).strip()
                    for fmt in ("%H:%M", "%H:%M:%S", "%I:%M %p", "%I:%M:%S %p"):
                        try:
                            hora_entrada = datetime.strptime(hora_str, fmt).time()
                            break
                        except Exception:
                            continue

                if not hora_entrada:
                    registros_ignorados += 1
                    continue

                # 💾 Criar nova presença (sem sobrescrever)
                if not Presenca.objects.filter(usuario=usuario, data_presenca=data_presenca).exists():
                    Presenca.objects.create(
                        usuario=usuario,
                        data_presenca=data_presenca,
                        hora_entrada=hora_entrada,
                        origem_registo='Importação Excel'
                    )
                    registros_importados += 1
                else:
                    registros_ignorados += 1  # já existia

            messages.success(request, f"{registros_importados} presenças importadas com sucesso para o dia {data_presenca.strftime('%d/%m/%Y')}.")
            if registros_ignorados:
                messages.warning(request, f"{registros_ignorados} registos foram ignorados (duplicados ou inválidos).")

            return redirect(reverse('formatura:upload_presenca'))

        except Exception as e:
            messages.error(request, f"Erro ao processar o ficheiro: {str(e)}")

    return render(request, 'formatura/upload_presenca.html', {
        'funcionario': funcionario,
        'form_action': reverse('formatura:upload_presenca'),
    }) 
    
    
'''  
@login_required(login_url='authors:login', redirect_field_name='next')
def listar_presencas(request):
    funcionario = get_object_or_404(Funcionario, author=request.user)

    # 🔹 Filtros
    nome_query = request.GET.get('nome', '').strip()
    departamento_id = request.GET.get('departamento', '').strip()
    startdate_query = request.GET.get('startdate', '').strip()
    enddate_query = request.GET.get('enddate', '').strip()

    # 🔹 Base query
    presencas = Presenca.objects.select_related(
        'usuario', 'usuario__funcionario', 'usuario__funcionario__departamento'
    ).all().order_by('-data_presenca', '-hora_entrada')

    # 🔹 Filtro por nome do funcionário
    if nome_query:
        presencas = presencas.filter(
            Q(usuario__funcionario__nome_completo__icontains=nome_query) |
            Q(usuario__first_name__icontains=nome_query) |
            Q(usuario__last_name__icontains=nome_query)
        )

    # 🔹 Filtro por departamento
    if departamento_id:
        presencas = presencas.filter(usuario__funcionario__departamento__id=departamento_id)

    # 🔹 Filtro por datas
    if startdate_query:
        try:
            startdate = datetime.strptime(startdate_query, "%Y-%m-%d").date()
            presencas = presencas.filter(data_presenca__gte=startdate)
        except ValueError:
            messages.warning(request, "Data inicial inválida. Use o formato AAAA-MM-DD.")

    if enddate_query:
        try:
            enddate = datetime.strptime(enddate_query, "%Y-%m-%d").date()
            presencas = presencas.filter(data_presenca__lte=enddate)
        except ValueError:
            messages.warning(request, "Data final inválida. Use o formato AAAA-MM-DD.")

    # 🔹 Contadores e resumo
    total_presencas = presencas.count()
    total_funcionarios = presencas.values('usuario').distinct().count()
    departamentos = Departamento.objects.all()

    context = {
        'funcionario': funcionario,
        'presencas': presencas,
        'total_presencas': total_presencas,
        'total_funcionarios': total_funcionarios,
        'nome_query': nome_query,
        'departamento_id': departamento_id,
        'startdate_query': startdate_query,
        'enddate_query': enddate_query,
        'departamentos': departamentos,
        'form_action': reverse('formatura:listar_presencas'),
    }

    return render(request, 'formatura/listar_presencas.html', context)
'''

@login_required(login_url='authors:login')
def relatorio_presencas(request):
    today = date.today()
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')

    funcionario = get_object_or_404(Funcionario, author=request.user)

    # 🔹 Definir período
    if startdate:
        startdate = datetime.strptime(startdate, "%Y-%m-%d").date()
    else:
        startdate = today.replace(day=1)

    if enddate:
        enddate = datetime.strptime(enddate, "%Y-%m-%d").date()
    else:
        enddate = today

    # 🔹 Buscar presenças no período
    presencas_no_periodo = Presenca.objects.filter(
        data_presenca__range=[startdate, enddate]
    ).select_related('usuario', 'usuario__funcionario', 'usuario__funcionario__departamento')

    # 🔹 Obter dias únicos onde houveram presenças
    dias_com_presenca = presencas_no_periodo.values_list('data_presenca', flat=True).distinct().order_by('data_presenca')

    # 🔹 Mapear presenças por usuário e dia para acesso rápido
    presencas_dict = {}
    for p in presencas_no_periodo:
        presencas_dict.setdefault(p.usuario_id, {})[p.data_presenca] = p

    # 🔹 Buscar todos os funcionários
    funcionarios = Funcionario.objects.select_related('departamento', 'author').filter(author__is_active=True)

    funcionarios = funcionarios.order_by('nome_completo')
    # 🔹 Monta relatório
    relatorio = []
    for func in funcionarios:
        linha = {
            'nome': func.nome_completo,
            'departamento': func.departamento.nome if func.departamento else '-',
            'presencas': []
        }
        for dia in dias_com_presenca:
            presenca = presencas_dict.get(func.author_id, {}).get(dia)
            if presenca:
                linha['presencas'].append(presenca.hora_entrada.strftime("%H:%M"))
            else:
                linha['presencas'].append('F')  # Faltou
        relatorio.append(linha)

    context = {
        'relatorio': relatorio,
        'funcionario': funcionario,
        'dias': dias_com_presenca,
        'form_action': reverse('formatura:relatorio_presencas'),
        'startdate': startdate,
        'enddate': enddate,
    }

    return render(request, 'formatura/relatorio_presencas.html', context)

@login_required(login_url='authors:login', redirect_field_name='next')
def listar_presencas(request):
    funcionario = get_object_or_404(Funcionario, author=request.user)

    # 🔹 Filtros do formulário
    nome_query = request.GET.get('nome', '').strip()
    departamento_id = request.GET.get('departamento', '').strip()
    startdate_query = request.GET.get('startdate', '').strip()
    enddate_query = request.GET.get('enddate', '').strip()
    status_presenca = request.GET.get('status', 'todos')  # todos, presentes, faltosos

    # 🔹 Definir período
    today = date.today()
    try:
        startdate = datetime.strptime(startdate_query, "%Y-%m-%d").date() if startdate_query else today.replace(day=1)
        enddate = datetime.strptime(enddate_query, "%Y-%m-%d").date() if enddate_query else today
    except ValueError:
        messages.warning(request, "Datas inválidas. Usando período padrão do mês atual.")
        startdate = today.replace(day=1)
        enddate = today

    # 🔹 QuerySet base de presenças no período
    presencas_qs = Presenca.objects.select_related('usuario', 'usuario__funcionario', 'usuario__funcionario__departamento') \
                                   .filter(data_presenca__range=(startdate, enddate))

    # 🔹 Lista de todos os funcionários (filtrando nome/departamento)
    funcionarios = Funcionario.objects.select_related('departamento', 'author').filter(author__is_active=True)

    if nome_query:
        funcionarios = funcionarios.filter(nome_completo__icontains=nome_query)
    if departamento_id:
        funcionarios = funcionarios.filter(departamento_id=departamento_id)

    # 🔹 Monta relatório completo
    dias = presencas_qs.values_list('data_presenca', flat=True).distinct().order_by('data_presenca')

    presencas_dict = {}
    for p in presencas_qs:
        presencas_dict.setdefault(p.usuario_id, {})[p.data_presenca] = p


    relatorio = []
    funcionarios = funcionarios.order_by('nome_completo')


    for func in funcionarios:
        linha = {
            'nome': func.nome_completo,
            'departamento': func.departamento.nome if func.departamento else '-',
            'presencas': []
        }
        for dia in dias:
            presenca = presencas_dict.get(func.author_id, {}).get(dia)
            if presenca:
                linha['presencas'].append({
                    'hora_entrada': presenca.hora_entrada.strftime("%H:%M") if presenca.hora_entrada else '-',
                    'origem_registo': presenca.origem_registo or '-',
                    'status': 'P'
                })
            else:
                linha['presencas'].append({
                    'hora_entrada': '-',
                    'origem_registo': '-',
                    'status': 'F'
                })

        # Filtro por status geral do funcionário
        if status_presenca == 'presentes' and all(p['status'] == 'F' for p in linha['presencas']):
            continue
        if status_presenca == 'faltosos' and all(p['status'] == 'P' for p in linha['presencas']):
            continue

        relatorio.append(linha)


    context = {
        'funcionario': funcionario,
        'relatorio': relatorio,
        'dias': dias,
        'departamentos': Departamento.objects.all().order_by('nome'),
        'nome_query': nome_query,
        'departamento_id': departamento_id,
        'startdate_query': startdate_query,
        'enddate_query': enddate_query,
        'status_presenca': status_presenca,
        'form_action': reverse('formatura:listar_presencas'),
    }

    return render(request, 'formatura/listar_presencas.html', context)


@login_required(login_url="authors:login", redirect_field_name="next")
@transaction.atomic
def cadastrar_formatura(request):

    # 🔹 Obtém dados do funcionário do usuário autenticado
    funcionario = get_object_or_404(Funcionario, author=request.user)

    if request.method == "POST":
        form = FormaturaForm(data=request.POST, files=request.FILES)
        formset = PontoAgendaFormSet(data=request.POST, files=request.FILES)

        if form.is_valid() and formset.is_valid():
            formatura = form.save(commit=False)

            # Auditoria
            if hasattr(formatura, "criado_por") and not formatura.pk:
                formatura.criado_por = request.user
            if hasattr(formatura, "atualizado_por"):
                formatura.atualizado_por = request.user

            formatura.ativo = True
            formatura.save()

            # Registrar histórico
            try:
                update_change_reason(formatura, "Formatura criada")
                formatura.save()
            except:
                pass

            # Processar pontos de agenda
            pontos = formset.save(commit=False)
            for ponto in pontos:
                ponto.formatura = formatura
                if hasattr(ponto, "criado_por") and not ponto.pk:
                    ponto.criado_por = request.user
                if hasattr(ponto, "atualizado_por"):
                    ponto.atualizado_por = request.user
                ponto.save()

            messages.success(request, "✅ Formatura cadastrada com sucesso!")
            return redirect(reverse("formatura:listar_formaturas"))
        else:
            messages.error(request, "⚠️ Dados inválidos. Verifique o formulário.")
    else:
        form = FormaturaForm()
        formset = PontoAgendaFormSet()

    return render(
        request,
        "formatura/cadastrar_formatura.html",
        {
            "form": form,
            "formset": formset,
            "funcionario": funcionario,
            "form_action": reverse("formatura:cadastrar_formatura"),
        },
    )
    
@login_required(login_url='authors:login', redirect_field_name='next')
def listar_formaturas(request):
    funcionario = get_object_or_404(Funcionario, author=request.user)

    # 🔹 Filtros GET
    titulo_query = request.GET.get('titulo', '').strip()
    local_query = request.GET.get('local', '').strip()
    startdate_query = request.GET.get('startdate', '').strip()
    enddate_query = request.GET.get('enddate', '').strip()

    # 🔹 Definir período
    today = date.today()
    try:
        startdate = datetime.strptime(startdate_query, "%Y-%m-%d").date() if startdate_query else None
        enddate = datetime.strptime(enddate_query, "%Y-%m-%d").date() if enddate_query else None
    except ValueError:
        messages.warning(request, "Datas inválidas. Usando período padrão do mês atual.")
        startdate = today.replace(day=1)
        enddate = today

    if startdate and enddate:
        formaturas = formaturas.filter(data__range=(startdate, enddate))
    elif startdate:
        formaturas = formaturas.filter(data__gte=startdate)
    elif enddate:
        formaturas = formaturas.filter(data__lte=enddate)
    
    formaturas = Formatura.objects.filter(
    Q(publicado=True) | Q(criado_por=request.user)
    )

    # Aplica filtro por data somente se startdate e enddate existirem
    if startdate and enddate:
        formaturas = formaturas.filter(data__range=(startdate, enddate))

    # Continua com select_related, prefetch_related e ordenação
    formaturas = formaturas.select_related('criado_por', 'atualizado_por') \
                        .prefetch_related(
                            Prefetch('pontos_agenda', queryset=PontoAgenda.objects.select_related('departamento', 'responsavel'))
                        ) \
                        .order_by("-data", "titulo")
    # 🔹 Query base
    # formaturas = (
    #     Formatura.objects.filter(
    #         Q(publicado=True) | Q(criado_por=request.user)
    #     )
    #     # .filter(data__range=(startdate, enddate))
    #     .filter(data__range=(startdate, enddate))
    #     .select_related()
    #     .order_by("-data", "titulo")
    # )

    # 🔹 Aplicação dos filtros
    if titulo_query:
        formaturas = formaturas.filter(titulo__icontains=titulo_query)

    if local_query:
        formaturas = formaturas.filter(local__icontains=local_query)

    # 🔹 Monta resultado
    linhas = []
    for form in formaturas:
        linhas.append({
            "id": form.id,
            "titulo": form.titulo or "-",
            "data": form.data,
            "local": form.local or "-",
            "total_tarefas": form.total_tarefas,
            "tarefas_concluidas": form.tarefas_concluidas,
            "progresso_percentual": form.progresso_percentual,
        })

    context = {
        "funcionario": funcionario,
        "linhas": linhas,
        "startdate_query": startdate_query,
        "enddate_query": enddate_query,
        "titulo_query": titulo_query,
        "local_query": local_query,
        "form_action": reverse("formatura:listar_formaturas"),
    }

    return render(request, "formatura/listar_formatura.html", context)


@login_required(login_url='authors:login', redirect_field_name='next')
def detalhes_formatura(request, id):
    funcionario = get_object_or_404(Funcionario, author=request.user)
    
    formatura = get_object_or_404(Formatura, id=id)

    # 🔹 Ordena pontos de agenda pelo campo 'ordem', depois prioridade
    pontos = formatura.pontos_agenda.select_related('departamento', 'responsavel').order_by('ordem', '-prioridade')

    context = {
        "funcionario": funcionario,
        "formatura": formatura,
        "pontos": pontos,
        "total_tarefas": formatura.total_tarefas,
        "tarefas_concluidas": formatura.tarefas_concluidas,
        "progresso_percentual": formatura.progresso_percentual,
        "voltar_url": reverse("formatura:listar_formaturas"),
       # "editar_url": reverse("formatura:editar_formatura", args=[formatura.id]),  # caso tenha tela de edição
    }

    return render(request, "formatura/detalhes_formatura.html", context)

@login_required(login_url='authors:login', redirect_field_name='next')
@transaction.atomic
def editar_formatura(request, pk):
    # funcionario = Funcionario.objects.filter(author=request.user).first()
    # if not funcionario:
    #     raise Http404("Funcionário não encontrado")

    funcionario = get_object_or_404(Funcionario, author=request.user)

    # ✅ Garantir que o user só edita se:
    #   - For superuser
    #   - Ou for o criador
    formatura = get_object_or_404(Formatura, pk=pk)

    # if not request.user.is_superuser and formatura.criado_por != request.user:
    #     messages.error(request, "⚠️ Não tem permissão para editar esta formatura.")
    #     return redirect(reverse("formatura:listar_formaturas"))

    # Carrega form e formset
    if request.method == "POST":
        form = FormaturaForm(data=request.POST, files=request.FILES, instance=formatura)
        formset = PontoAgendaFormSet(data=request.POST, files=request.FILES, instance=formatura)
        print("FORM ERRORS:", form.errors)
        print("FORMSET ERRORS:", formset.errors)

        if form.is_valid() and formset.is_valid():
            print("✅ FORM VALID, BEFORE SAVE:", formatura.__dict__)
            formatura = form.save(commit=False)

            # 🔹 Auditoria
            if hasattr(formatura, "atualizado_por"):
                formatura.atualizado_por = request.user

            formatura.save()

            formset.save()

            # Registrar histórico
            try:
                update_change_reason(formatura, "Formatura atualizada")
                formatura.save()
            except:
                pass

            messages.success(request, "✅ Formatura atualizada com sucesso!")
            return redirect(reverse("formatura:listar_formaturas"))
        else:
            messages.error(request, "⚠️ Alguns dados são inválidos. Verifique o formulário.")
    else:
        form = FormaturaForm(instance=formatura)
        formset = PontoAgendaFormSet(instance=formatura)

    return render(
        request,
        "formatura/editar_formatura.html",
        {
            "form": form,
            "formset": formset,
            "formatura": formatura,
            "funcionario": funcionario,
            "form_action": reverse("formatura:editar_formatura", kwargs={"pk": pk}),
        },
    )