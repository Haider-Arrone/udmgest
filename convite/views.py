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
    Fluxo em 2 passos:
      1) Usuario insere codigo_convite;
      2) Se o codigo for valido e pertencer ao evento e nao estiver usado,
         mostra o form para nome/contacto/lugares e permite confirmar.
    """

    evento = get_object_or_404(Evento, id=evento_id)
    convite = None
    form = None
    step = request.POST.get('step') if request.method == 'POST' else None

    # POST passo 1: validar codigo
    if request.method == 'POST' and step == 'check_code':
        codigo = request.POST.get('codigo_convite', '').strip().upper()
        if not codigo:
            messages.error(request, "Por favor informe o código do convite.")
        else:
            try:
                convite = Convite.objects.get(evento=evento, codigo_convite=codigo)
            except Convite.DoesNotExist:
                convite = None
                messages.error(request, "Código inválido ou não pertence a este evento.")
            else:
                # convite encontrado
                if convite.status == Convite.Status.PRESENTE or convite.status == Convite.Status.CONFIRMADO:
                    messages.warning(request, "Este convite já foi utilizado.")
                    # podemos ainda mostrar os dados do convite (readonly) se quiser
                    convite = None
                else:
                    # prepara o form com a instancia do convite (preenche campos vazios)
                    form = ConfirmarPresencaForm(instance=convite)

    # POST passo 2: confirmar o preenchimento (nome/contacto/lugares)
    elif request.method == 'POST' and step == 'confirm':
        codigo = request.POST.get('codigo_convite', '').strip().upper()
        if not codigo:
            messages.error(request, "Código não informado. Volte a inserir o código.")
        else:
            try:
                convite = Convite.objects.get(evento=evento, codigo_convite=codigo)
            except Convite.DoesNotExist:
                messages.error(request, "Código inválido ou não pertence a este evento.")
                convite = None
            else:
                if convite.status == Convite.Status.PRESENTE or convite.status == Convite.Status.CONFIRMADO:
                    messages.warning(request, "Este convite já foi utilizado.")
                    convite = None
                else:
                    # usa o form com instance=convite para validar e salvar
                    form = ConfirmarPresencaForm(request.POST, instance=convite)
                    if form.is_valid():
                        convite = form.save(commit=False)
                        convite.status = Convite.Status.CONFIRMADO
                        # se preferir marcar presença imediata, usar marcar_presenca()
                        # convite.marcar_presenca()
                        convite.save()
                        messages.success(request, "Sua presença foi registrada com sucesso!")
                        # opcional: redirecionar para página de confirmação ou mostrar resumo aqui
                        return redirect('convite:confirmar_presenca', evento_id=evento.id)
                    else:
                        messages.error(request, "Corrija os erros no formulário e tente novamente.")

    # GET ou POST sem step válido -> mostra apenas o input de código
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

        # 🔍 1 — Verificar se esse código já foi usado nesse mesmo evento
        if Convite.objects.filter(evento=evento, codigo_estudante=codigo_estudante).exists():
            messages.error(
                request,
                "Este código de estudante já possui um convite associado a este evento."
            )
            return redirect(request.path)

        # 🔁 2 — Gerar um código de convite realmente único
        def gerar_codigo_unico():
            while True:
                codigo = str(uuid.uuid4()).split('-')[0].upper()
                if not Convite.objects.filter(codigo_convite=codigo).exists():
                    return codigo

        codigo_convite = gerar_codigo_unico()

        # 📝 3 — Criar o convite
        convite = Convite.objects.create(
            evento=evento,
            codigo_estudante=codigo_estudante,
            codigo_convite=codigo_convite,
            status=Convite.Status.PENDENTE
        )

        messages.success(
            request,
            f"Convite gerado com sucesso! Código do convite: {codigo_convite}"
        )

        return redirect("convite:detalhes_convite", convite_id=convite.id)

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
    print(codigo_convite)
    # --- Validar campos obrigatórios ---
    if not codigo_convite:
        return JsonResponse({"success": False, "message": "Código do convite é obrigatório."}, status=400)

    if not nome_completo or not contacto:
        return JsonResponse({"success": False, "message": "Nome e contacto são obrigatórios."}, status=400)

    # --- Buscar convite ---
    try:
        convite = Convite.objects.get(codigo_convite=codigo_convite)
    except Convite.DoesNotExist:
        return JsonResponse({"success": False, "message": "Código inválido."}, status=404)

    # --- Verificar se já está usado ---
    if convite.status in [Convite.Status.CONFIRMADO, Convite.Status.PRESENTE]:
        return JsonResponse({
            "success": False,
            "message": "Este convite já foi utilizado."
        }, status=400)

    # --- Atualizar convite ---
    convite.nome_completo = nome_completo
    convite.contacto = contacto
    # convite.lugares_reservados = int(lugares)
    convite.status = Convite.Status.CONFIRMADO
    convite.presente_em = timezone.now()
    convite.save()

    # --- Resposta ---
    return JsonResponse({
        "success": True,
        "message": "Presença confirmada com sucesso!",
        "convite": {
            "codigo_convite": convite.codigo_convite,
            "nome_completo": convite.nome_completo,
            "contacto": convite.contacto,
            "lugares_reservados": convite.lugares_reservados,
            "status": convite.status,
            "presente_em": convite.presente_em.isoformat(),
        },
        "evento": {
            "titulo": convite.evento.titulo if convite.evento else None,
            "data": convite.evento.data.isoformat() if convite.evento and convite.evento.data else None,
            "local": convite.evento.local if convite.evento else None
        }
    })
    
def pagina_simples(request):
    return render(request, "convite/index.html")
