from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from .models import Evento, Convite
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from convite.forms.convite_form import ConfirmarPresencaForm
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
import uuid
from django.utils import timezone
from django.http import Http404
from expedient.models import  Funcionario
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

def marcar_presenca_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    convites = evento.convites.all().order_by('nome_completo')

    if request.method == 'POST':
        convite_id = request.POST.get('convite_id')
        convite = get_object_or_404(Convite, id=convite_id)
        convite.marcar_presenca()
        messages.success(request, f"Presença de {convite.nome_completo or 'Convidado sem nome'} registrada.")
        return redirect(reverse('marcar_presenca_evento', args=[evento.id]))

    context = {
        'evento': evento,
        'convites': convites
    }
    return render(request, 'convite/confirmar_presenca.html', context)

def confirmar_presenca(request, evento_id):
    """
    Confirmação de presença para códigos que podem ter até 2 convites.
    """
    evento = get_object_or_404(Evento, id=evento_id)
    convite = None
    form = None
    step = request.POST.get('step') if request.method == 'POST' else None

    if request.method == 'POST' and step == 'check_code':
        codigo = request.POST.get('codigo_convite', '').strip().upper()
        if not codigo:
            messages.error(request, "Informe o código do convite.")
        else:
            # Busca convites disponíveis (PENDENTE) para este código
            convites_disponiveis = Convite.objects.filter(
                evento=evento,
                codigo_convite=codigo
            ).exclude(status__in=[Convite.Status.CONFIRMADO, Convite.Status.PRESENTE])

            if not convites_disponiveis.exists():
                messages.warning(request, "Todos os convites deste código já foram utilizados.")
            else:
                # Pega o primeiro convite disponível
                convite = convites_disponiveis.first()
                form = ConfirmarPresencaForm(instance=convite)

    elif request.method == 'POST' and step == 'confirm':
        codigo = request.POST.get('codigo_convite', '').strip().upper()
        if not codigo:
            messages.error(request, "Código não informado.")
        else:
            convites_disponiveis = Convite.objects.filter(
                evento=evento,
                codigo_convite=codigo
            ).exclude(status__in=[Convite.Status.CONFIRMADO, Convite.Status.PRESENTE])

            if not convites_disponiveis.exists():
                messages.warning(request, "Todos os convites deste código já foram utilizados.")
            else:
                convite = convites_disponiveis.first()
                form = ConfirmarPresencaForm(request.POST, instance=convite)
                if form.is_valid():
                    convite = form.save(commit=False)
                    convite.status = Convite.Status.CONFIRMADO
                    convite.save()
                    messages.success(request, "Presença registrada com sucesso!")
                    # Atualiza o convite e form para o próximo disponível (se houver)
                    convites_disponiveis = Convite.objects.filter(
                        evento=evento,
                        codigo_convite=codigo
                    ).exclude(status__in=[Convite.Status.CONFIRMADO, Convite.Status.PRESENTE])
                    if convites_disponiveis.exists():
                        convite = convites_disponiveis.first()
                        form = ConfirmarPresencaForm(instance=convite)
                    else:
                        convite = None
                        form = None
                else:
                    messages.error(request, "Corrija os erros no formulário e tente novamente.")

    context = {
        'evento': evento,
        'convite': convite,
        'form': form,
    }
    return render(request, 'convite/confirmar_presenca.html', context)


@login_required(login_url='authors:login', redirect_field_name='next')
def listar_convites(request, evento_id=None):
    """
    Lista convites com pesquisa e paginação.
    Se evento_id for fornecido, filtra os convites desse evento.
    """
    funcionario = Funcionario.objects.select_related('departamento').filter(author=request.user).first()
    
    if not funcionario:
        raise Http404("Funcionário não encontrado")

    evento = None
    convites = Convite.objects.all().order_by('-criado_em')

    # Filtrar por evento, se informado
    if evento_id:
        evento = get_object_or_404(Evento, id=evento_id)
        convites = convites.filter(evento=evento)

    # Pesquisa
    query = request.GET.get("q")
    if query:
        convites = convites.filter(
            Q(nome_completo__icontains=query) |
            Q(contacto__icontains=query) |
            Q(codigo_convite__icontains=query) |
            Q(codigo_estudante__icontains=query)
        )

    # Paginação
    paginator = Paginator(convites, 20)  # 20 por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "evento": evento,
        "convites": page_obj,
        "page_obj": page_obj,
        "query": query,
        'funcionario': funcionario,
    }

    return render(request, "convite/listar_convites.html", context)

@login_required(login_url='authors:login', redirect_field_name='next')
def detalhes_convite(request, convite_id):
    """
    Mostra os detalhes de um convite específico, incluindo informações do evento.
    """
    funcionario = Funcionario.objects.select_related('departamento').filter(author=request.user).first()
    
    if not funcionario:
        raise Http404("Funcionário não encontrado")
    convite = get_object_or_404(Convite, id=convite_id)
    
    context = {
        "convite": convite,
        "evento": convite.evento,
        'funcionario': funcionario,
    }
    
    return render(request, "convite/detalhes_convite.html", context)


@login_required(login_url='authors:login', redirect_field_name='next')
def gerar_convite(request):
    funcionario = Funcionario.objects.select_related('departamento').filter(author=request.user).first()
    
    if not funcionario:
        raise Http404("Funcionário não encontrado")
    
    eventos = Evento.objects.all().order_by("-data")

    if request.method == "POST":
        evento_id = request.POST.get("evento_id")
        codigo_estudante = request.POST.get("codigo_estudante", "").strip()

        if not evento_id:
            messages.error(request, "Selecione um evento.")
            return redirect(request.path)

        if not codigo_estudante:
            messages.error(request, "Informe o código do estudante.")
            return redirect(request.path)

        evento = get_object_or_404(Evento, id=evento_id)

        # 🔍 Verificar se já tem convites
        convites_existentes = Convite.objects.filter(
            evento=evento,
            codigo_estudante=codigo_estudante
        )

        if convites_existentes.exists():
            messages.error(
                request,
                "Este estudante já possui convites associados a este evento."
            )
            return redirect(request.path)

        # 🔁 Gerar código único
        def gerar_codigo_unico():
            while True:
                codigo = str(uuid.uuid4()).split('-')[0].upper()
                if not Convite.objects.filter(codigo_convite=codigo).exists():
                    return codigo

        codigo_convite = gerar_codigo_unico()

        # 📝 Criar os dois convites de uma vez
        convite1 = Convite.objects.create(
            evento=evento,
            codigo_estudante=codigo_estudante,
            codigo_convite=codigo_convite,
            status=Convite.Status.PENDENTE
        )

        convite2 = Convite.objects.create(
            evento=evento,
            codigo_estudante=codigo_estudante,
            codigo_convite=codigo_convite,
            status=Convite.Status.PENDENTE
        )

        messages.success(
            request,
            f"Foram criados 2 convites! Código do convite: {codigo_convite}"
        )

        # Pode redirecionar para o primeiro, ou para uma lista
        return redirect("convite:detalhes_convite", convite_id=convite1.id)

    return render(request, "convite/gerar_codigo_convite.html", {
        "eventos": eventos,
        'funcionario': funcionario,
    })


    
@csrf_exempt
def confirmar_presenca_externa(request):
    """Recebe uma única solicitação com todos os dados e retorna uma única resposta."""
    
    if request.method != "POST":
        return HttpResponseBadRequest("Use POST para enviar dados.")

    codigo_convite = request.POST.get("codigo_convite", "").strip().upper()
    nome_completo = request.POST.get("nome_completo", "").strip()
    contacto = request.POST.get("contacto", "").strip()
    # lugares = request.POST.get("lugares_reservados", "1").strip()

    # --- Validar campos obrigatórios ---
    if not codigo_convite:
        return JsonResponse({"success": False, "message": "Código do convite é obrigatório."}, status=400)

    if not nome_completo or not contacto:
        return JsonResponse({"success": False, "message": "Nome e contacto são obrigatórios."}, status=400)

    # --- Buscar convites pelo código (pode ter até 2) ---
    convites = Convite.objects.filter(codigo_convite=codigo_convite).order_by('id')

    if not convites.exists():
        return JsonResponse({"success": False, "message": "Código inválido."}, status=404)

    # --- Encontrar o primeiro convite não utilizado ---
    convite_para_confirmar = None
    for c in convites:
        if c.status not in [Convite.Status.CONFIRMADO, Convite.Status.PRESENTE]:
            convite_para_confirmar = c
            break

    if not convite_para_confirmar:
        return JsonResponse({
            "success": False,
            "message": "Todos os convites desse código já foram utilizados."
        }, status=400)

    # --- Atualizar convite ---
    convite_para_confirmar.nome_completo = nome_completo
    convite_para_confirmar.contacto = contacto
    # convite_para_confirmar.lugares_reservados = int(lugares)
    convite_para_confirmar.status = Convite.Status.CONFIRMADO
    convite_para_confirmar.presente_em = timezone.now()
    convite_para_confirmar.save()

    # --- Resposta ---
    return JsonResponse({
        "success": True,
        "message": "Presença confirmada com sucesso!",
        "convite": {
            "codigo_convite": convite_para_confirmar.codigo_convite,
            "nome_completo": convite_para_confirmar.nome_completo,
            "contacto": convite_para_confirmar.contacto,
            "lugares_reservados": convite_para_confirmar.lugares_reservados,
            "status": convite_para_confirmar.status,
            "presente_em": convite_para_confirmar.presente_em.isoformat(),
        },
        "evento": {
            "titulo": convite_para_confirmar.evento.titulo if convite_para_confirmar.evento else None,
            "data": convite_para_confirmar.evento.data.isoformat() if convite_para_confirmar.evento and convite_para_confirmar.evento.data else None,
            "local": convite_para_confirmar.evento.local if convite_para_confirmar.evento else None
        }
    })
    
def pagina_simples(request):
    return render(request, "convite/index.html")

@login_required(login_url='authors:login', redirect_field_name='next')
def editar_convite(request, convite_id):
    funcionario = Funcionario.objects.select_related('departamento').filter(author=request.user).first()
    if not funcionario:
        raise Http404("Funcionário não encontrado")

    convite = get_object_or_404(Convite, id=convite_id)

    if request.method == "POST":
        # Capturar dados do POST manualmente
        convite.nome_completo = request.POST.get("nome_completo")
        convite.contacto = request.POST.get("contacto")
        # convite.codigo_convite = request.POST.get("codigo_convite")
        # convite.codigo_estudante = request.POST.get("codigo_estudante")
        convite.lugares_reservados = request.POST.get("lugares_reservados")
        convite.status = request.POST.get("status")
          # FK

        # Salvar
        convite.save()

        messages.success(request, "Convite atualizado com sucesso!")
        return redirect("convite:listar_convites")

    # Se GET → exibir formulário manualmente
    eventos = Evento.objects.all().order_by("-data")

    context = {
        "funcionario": funcionario,
        "convite": convite,
        "eventos": eventos,
    }

    return render(request, "convite/editar_convite.html", context)