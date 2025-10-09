from django.shortcuts import render, get_object_or_404
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Presenca
from expedient.models import Funcionario, Departamento  # importa o modelo Funcionario
from datetime import datetime, date
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta

# Create your views here.
def upload_presenca(request):
    funcionario = get_object_or_404(Funcionario, author=request.user) 
    if request.method == "POST" and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']

        try:
            
            # 📘 Lê o ficheiro Excel
            df = pd.read_excel(excel_file, engine='openpyxl')

            # 🔹 Remove linhas e colunas vazias
            df = df.dropna(axis=0, how='all').dropna(axis=1, how='all')

            # 🔹 Confirma colunas essenciais
            colunas_esperadas = ['Employee ID', 'Name', 'Department']
            for coluna in colunas_esperadas:
                if coluna not in df.columns:
                    messages.error(request, f"Coluna '{coluna}' não encontrada no ficheiro.")
                    return redirect('upload_presenca')

            # 🔹 Detecta a coluna do dia (a única que varia)
            dia_coluna = next((c for c in df.columns if c not in colunas_esperadas), None)
            if not dia_coluna:
                messages.error(request, "Não foi encontrada a coluna correspondente ao dia do mês.")
                return redirect('upload_presenca')

            registros_importados = 0
            registros_ignorados = 0

            # 🔁 Itera sobre as linhas do ficheiro
            for index, row in df.iterrows():
                employee_id = row.get('Employee ID')
                hora_val = row.get(dia_coluna)

                if pd.isnull(employee_id) or pd.isnull(hora_val):
                    registros_ignorados += 1
                    continue

                # 🔹 Verifica se o usuário existe
                try:
                    usuario = User.objects.get(pk=int(employee_id))
                    funcionario_registro  = Funcionario.objects.get(author=usuario)
                except User.DoesNotExist:
                    registros_ignorados += 1
                    messages.warning(request, f"Usuário com ID {employee_id} não encontrado (linha {index + 2}).")
                    continue
                except Funcionario.DoesNotExist:
                    registros_ignorados += 1
                    messages.warning(request, f"Funcionário para o usuário {employee_id} não encontrado (linha {index + 2}).")
                    continue

                # 🕒 Processa a hora
                hora_entrada = None

                # Caso já seja datetime ou Timestamp (Excel interpreta como hora)
                if hasattr(hora_val, "time"):
                    try:
                        hora_entrada = hora_val.time()
                    except Exception:
                        hora_entrada = None

                # Caso seja string
                if hora_entrada is None:
                    hora_str = str(hora_val).strip().replace("\n", " ").replace("\r", "")
                    parsed = None
                    formatos_possiveis = ("%H:%M", "%H:%M:%S", "%H.%M", "%I:%M %p", "%I:%M:%S %p")

                    for fmt in formatos_possiveis:
                        try:
                            parsed = datetime.strptime(hora_str, fmt).time()
                            break
                        except Exception:
                            continue

                    # Fallback automático do pandas
                    if parsed is None:
                        try:
                            ts = pd.to_datetime(hora_str, errors="coerce")
                            if not pd.isnull(ts):
                                parsed = ts.time()
                        except Exception:
                            parsed = None

                    if parsed is None:
                        registros_ignorados += 1
                        messages.warning(request, f"Hora inválida na linha {index + 2}: {hora_str}")
                        continue

                    hora_entrada = parsed

                # 🗓 Cria a data de presença com base no nome da coluna
                today = date.today()
                try:
                    dia = int(str(dia_coluna).strip())
                    data_presenca = date(today.year, today.month, dia)
                except ValueError:
                    messages.error(request, f"Coluna '{dia_coluna}' não é um número válido de dia.")
                    return redirect('upload_presenca')

                # 💾 Cria ou atualiza presença
                Presenca.objects.update_or_create(
                    usuario=usuario,
                    data_presenca=data_presenca,
                    defaults={
                        'hora_entrada': hora_entrada,
                        'origem_registo': 'Importação Excel'
                    }
                )
                registros_importados += 1

            # ✅ Mensagens de sucesso/falha
            messages.success(request, f"{registros_importados} registros importados com sucesso!")
            if registros_ignorados:
                messages.warning(request, f"{registros_ignorados} registros foram ignorados por erro ou falta de dados.")

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
    # Seleciona o período (mês atual como padrão)
    today = date.today()
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    
    funcionario = get_object_or_404(Funcionario, author=request.user)

    if startdate:
        startdate = datetime.strptime(startdate, "%Y-%m-%d").date()
    else:
        startdate = today.replace(day=1)

    if enddate:
        enddate = datetime.strptime(enddate, "%Y-%m-%d").date()
    else:
        enddate = today

    # Lista de dias do período
    delta = enddate - startdate
    dias = [startdate + timedelta(days=i) for i in range(delta.days + 1)]

    funcionarios = Funcionario.objects.select_related('departamento').all()

    # Monta o relatório
    relatorio = []
    for func in funcionarios:
        linha = {
            'nome': func.nome_completo,
            'departamento': func.departamento.nome if func.departamento else '-',
            'presencas': []
        }
        for dia in dias:
            presenca = Presenca.objects.filter(usuario=func.author, data_presenca=dia).first()
            if presenca:
                linha['presencas'].append(presenca.hora_entrada.strftime("%H:%M"))
            else:
                linha['presencas'].append('F')  # F = Faltou
        relatorio.append(linha)

    context = {
        'relatorio': relatorio,
        'funcionario': funcionario,
        'dias': dias,
        'form_action': reverse('formatura:relatorio_presencas'),
    }

    return render(request, 'formatura/relatorio_presencas.html', context)

@login_required(login_url='authors:login', redirect_field_name='next')
def listar_presencas(request):
    # Usuário logado
    funcionario = get_object_or_404(Funcionario, author=request.user)

    # 🔹 Filtros do formulário
    nome_query = request.GET.get('nome', '').strip()
    departamento_id = request.GET.get('departamento', '').strip()
    startdate_query = request.GET.get('startdate', '').strip()
    enddate_query = request.GET.get('enddate', '').strip()
    status_presenca = request.GET.get('status', 'todos')  # todos, presentes, faltosos

    # 🔹 QuerySet base de presenças
    presencas_qs = Presenca.objects.select_related(
        'usuario', 'usuario__funcionario', 'usuario__funcionario__departamento'
    )

    # 🔹 Filtrar por datas
    if startdate_query:
        try:
            startdate = datetime.strptime(startdate_query, "%Y-%m-%d").date()
            presencas_qs = presencas_qs.filter(data_presenca__gte=startdate)
        except ValueError:
            messages.warning(request, "Data inicial inválida. Use o formato AAAA-MM-DD.")

    if enddate_query:
        try:
            enddate = datetime.strptime(enddate_query, "%Y-%m-%d").date()
            presencas_qs = presencas_qs.filter(data_presenca__lte=enddate)
        except ValueError:
            messages.warning(request, "Data final inválida. Use o formato AAAA-MM-DD.")

    # 🔹 Lista de todos os funcionários
    funcionarios = Funcionario.objects.select_related('departamento').all()

    # 🔹 Lista final de dados padronizados para o template
    tabela_presencas = []

    for func in funcionarios:
        # Filtrar por nome
        if nome_query and nome_query.lower() not in func.nome_completo.lower():
            continue

        # Filtrar por departamento
        if departamento_id and (not func.departamento or str(func.departamento.id) != departamento_id):
            continue

        # Buscar presença do funcionário no período filtrado
        presenca = presencas_qs.filter(usuario=func.author).first()

        # Filtrar por status
        if status_presenca == 'presentes' and not presenca:
            continue
        if status_presenca == 'faltosos' and presenca:
            continue

        tabela_presencas.append({
            'nome': func.nome_completo,
            'departamento': func.departamento.nome if func.departamento else '-',
            'data_presenca': presenca.data_presenca if presenca else '-',
            'hora_entrada': presenca.hora_entrada if presenca else '-',
            'origem_registo': presenca.origem_registo if presenca else '-',
        })

    context = {
        'funcionario': funcionario,
        'tabela_presencas': tabela_presencas,
        'total_funcionarios': funcionarios.count(),
        'total_registros': len(tabela_presencas),
        'nome_query': nome_query,
        'departamento_id': departamento_id,
        'startdate_query': startdate_query,
        'enddate_query': enddate_query,
        'departamentos': Departamento.objects.all(),
        'status_presenca': status_presenca,
        'form_action': reverse('formatura:listar_presencas'),
    }

    return render(request, 'formatura/listar_presencas.html', context)