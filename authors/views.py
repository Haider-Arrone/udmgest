
import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from expedient.models import Expedient, Funcionario, Parecer, Protocolo, Departamento
from expedient.views import expedient
from utils.expedient.pagination import make_pagination
from django.utils import timezone
import authors
from authors.forms.expedient_form import AuthorExpedientForm
from authors.forms.protocol_form import AuthorProtocolForm
from authors.forms.parecer_form import ParecerForm
from authors.forms.parecer_responder_form import Parecer_Responder_Form
from authors.forms.register_form import RegisterFormProfile
from authors.models import Profile

from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm
from expedient.filters import Expedient_filter, Protocol_filter
from utils.send_emails import enviar_email, enviar_email_novo_protocolo, enviar_email_protocolo_confirmado, enviar_email_resposta_expediente
# Create your views here.
PER_PAGE = int(os.environ.get('PER_PAGE', 10))


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    form_profile = RegisterFormProfile(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
                  'form': form,
                  'form_profile': form_profile,
                  'form_action': reverse('authors:create'),

                  })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    form_profile = RegisterFormProfile(POST)
    if form.is_valid() and form_profile.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        profile = form_profile.save(commit=False)
        profile.author = user
        profile.save()

        messages.success(request, 'Usuário criado com sucesso, faça o Login')

        del (request.session['register_form_data'])
        return redirect(reverse('authors:login'))
    return redirect('authors:register')


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('authors:dashbord'))
    else:
        form = LoginForm()
        return render(request, 'authors/pages/login.html', {
            'form': form,
            'form_action': reverse('authors:login_create')
        })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_url = reverse('authors:login')
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )

        if authenticated_user is not None:
            messages.success(request, 'Estás logado no sistema')
            login(request, authenticated_user)
            return redirect(reverse('authors:dashbord'))
        else:
            messages.error(request, 'Credencial inválida')

    else:
        messages.error(request, 'Nome de usuário ou senha inválidos')
    return redirect(login_url)


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord(request):
    expedients = Expedient.objects.filter(estado='Respondido',
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


'''
@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_expedient_edit(request, id):
    expedient = Expedient.objects.filter(recebido=False,
                                         usuario=request.user,
                                         pk=id
                                         ).first()
    if not expedient:
        raise Http404()

    form = AuthorExpedientForm(data=request.POST or None,
                               files=request.FILES or None,
                               instance=expedient)

    if form.is_valid():
        expedient = form.save(commit=False)

        expedient.usuario = request.user
        expedient.estado = 'Novo'
        # expedient.data_emissao = auto_now

        expedient.save()

        messages.success(request, 'Expediente salvo com sucesso!')
        return redirect(reverse('authors:dashbord_expedient_edit', args=(id,)))

    return render(request,
                  'authors/pages/dashbord_expedient.html',
                  {
                      'form': form
                  }
                  )

'''


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_expedient_new(request,):
    funcionario = Funcionario.objects.filter(author=request.user).first()
    form = AuthorExpedientForm(data=request.POST or None,
                               files=request.FILES or None,
                               )

    if form.is_valid():
        expedient = form.save(commit=False)

        expedient.usuario = request.user
        expedient.estado = 'Novo'
        # expedient.data_emissao = auto_now
        expedient.numero_Ex = 123
        expedient.save()

        messages.success(request, 'Expediente salvo com sucesso!')
        return redirect(reverse('authors:dashbord_expedient_emitidos'))

    return render(request,
                  'authors/pages/dashbord_expedient.html',
                  {
                      'form': form,
                      'funcionario': funcionario,
                      'form_action': reverse('authors:dashbord_expedient_new')
                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_expedient_emitidos(request):
    expedients = Expedient.objects.filter(
        usuario=request.user,

    ).exclude(estado='Respondido')
    funcionario = Funcionario.objects.filter(author=request.user).first()
    page_obj, pagination_range = make_pagination(
        request, expedients, PER_PAGE)

    return render(request,
                  'authors/pages/dashbord_emitidos.html', context={
                      'expedients': page_obj,
                      'pagination_range': pagination_range,
                      'funcionario': funcionario,

                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_expedient_recebidos(request):
    expedients = Expedient.objects.filter(recebido=True, estado='Respondido',
                                          usuario=request.user,

                                          )
    funcionario = Funcionario.objects.filter(author=request.user).first()
    page_obj, pagination_range = make_pagination(
        request, expedients, PER_PAGE)

    return render(request,
                  'authors/pages/dashbord_recebidos.html', context={
                      'expedients': page_obj,
                      'pagination_range': pagination_range,
                      'funcionario': funcionario,

                  }
                  )


'''
@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_expedient_see(request, id):
    expedient = Expedient.objects.filter(
        usuario=request.user,
        pk=id
    ).first()
    if not expedient:
        raise Http404()

    form = AuthorExpedientForm(data=request.POST or None,
                               files=request.FILES or None,
                               instance=expedient)

    return render(request,
                  'authors/pages/dashbord_expedient.html',
                  {
                      'form': form
                  }
                  )
'''


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_expedient_recebidos_funcionario(request):
    id_departamento = Funcionario.objects.get(author=request.user)
    departamento1 = id_departamento.departamento
    print(departamento1)
    funcionario = Funcionario.objects.filter(author=request.user).first()
    expedients = Expedient.objects.filter(departamento=departamento1,

                                          ).exclude(estado='Respondido')
    expedients = expedients.order_by('-id')  
    page_obj, pagination_range = make_pagination(
        request, expedients, PER_PAGE)

    return render(request,
                  'authors/pages/dashbord_recebidos_funcionario.html', context={
                      'expedients': page_obj,
                      'pagination_range': pagination_range,
                      'funcionario': funcionario,

                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_expedient_encaminhados_funcionario(request):
    id_departamento = Funcionario.objects.get(author=request.user)
    departamento1 = id_departamento.departamento
    print(id_departamento)
    funcionario = Funcionario.objects.filter(author=request.user).first()
    # parecer = Parecer.objects.filter(id_expedient__expedients, id_receptor=id_departamento)
    expedients = Expedient.objects.filter(estado='Encaminhado', parecer__id_receptor=departamento1, parecer__tipo='Encaminhar',


                                          ).exclude(estado='Respondido')
    page_obj, pagination_range = make_pagination(
        request, expedients, PER_PAGE)

    return render(request,
                  'authors/pages/dashbord_encaminhados_funcionario.html', context={
                      'expedients': page_obj,
                      'pagination_range': pagination_range,
                      'funcionario': funcionario,

                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_expedient_encaminhados_submetidos_funcionario(request):
    id_departamento = Funcionario.objects.get(author=request.user)
    departamento1 = id_departamento.departamento
    print(id_departamento)
    funcionario = Funcionario.objects.filter(author=request.user).first()
    # parecer = Parecer.objects.filter(id_expedient__expedients, id_receptor=id_departamento)
    expedients = Expedient.objects.filter(estado='Encaminhado', parecer__id_emissor=departamento1, parecer__tipo='Encaminhar',


                                          ).exclude(estado='Respondido')
    page_obj, pagination_range = make_pagination(
        request, expedients, PER_PAGE)

    return render(request,
                  'authors/pages/dashbord_encaminhados_submetidos_funcionario.html', context={
                      'expedients': page_obj,
                      'pagination_range': pagination_range,
                      'funcionario': funcionario,

                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_expedient_detail(request, id):
    expedient = Expedient.objects.filter(
        pk=id
    ).first()
    if not expedient:
        raise Http404()

    form = AuthorExpedientForm(data=request.POST or None,
                               files=request.FILES or None,
                               instance=expedient)
    usuario = expedient.usuario
    print(usuario)
    #id_departamento = Funcionario.objects.filter(author=request.user).first()
    # print(id_departamento.departamento)

    parecer = Parecer.objects.filter(id_expedient=id)
    profile = Profile.objects.filter(author=usuario).first()
    funcionario = Funcionario.objects.filter(author=request.user).first()
    funcionario_expedient = Funcionario.objects.filter(author=usuario).first()
    return render(request,
                  'authors/pages/expedient-detail.html',
                  context={'expedient': expedient, 'parecer': parecer,
                           'profile': profile, 'funcionario': funcionario,
                           'funcionario_expedient': funcionario_expedient}
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_expedient_ver_user(request, id):
    expedient = Expedient.objects.filter(
        pk=id
    ).first()

    if not expedient:
        raise Http404()

    form = AuthorExpedientForm(data=request.POST or None,
                               files=request.FILES or None,
                               instance=expedient)
    usuario = expedient.usuario
    print(usuario)
    funcionario = Funcionario.objects.filter(author=request.user).first()
    profile = Profile.objects.filter(author=usuario).first()
    funcionario_expedient = Funcionario.objects.filter(author=usuario).first()
    return render(request,
                  'authors/pages/expedient-user.html',
                  context={'expedient': expedient,
                           'profile': profile, 'funcionario': funcionario,
                           'funcionario_expedient': funcionario_expedient}
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_expedient_parecer(request, id, tipo):
    print(tipo)
    expedients = Expedient.objects.filter(pk=id).first()

    form = ParecerForm(data=request.POST or None,
                       files=request.FILES or None,
                       )

    if form.is_valid():
        parecer = form.save(commit=False)
        print(id)
        # parecer.id_expedient = expedients.
        # if(tipo=='responder'):
        #   parecer.id_receptor = expedients.
        #  expedients.estado = 'Respondido'
        # else:
        #   expedients.estado = 'Encaminhado'
        expedients.recebido = True
        expedients.save()
        # expedient.estado = 'Novo'
        # expedient.data_emissao = auto_now
       # expedient.numero_Ex = 123
        parecer.save()

        messages.success(request, 'Parecer submetido com sucesso!')
        return redirect(reverse('authors:dashbord_expedient_recebidos_funcionario'))

    return render(request,
                  'authors/pages/expedient-parecer.html',
                  {
                      'form': form,
                      'form_action': reverse('authors:dashbord_expedient_parecer', args=(id, tipo))
                  }
                  )

# Respondidos Funcionarios


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_expedient_respondidos_funcionario(request):
    id_departamento = Funcionario.objects.get(author=request.user)
    departamento1 = id_departamento.departamento
    print(departamento1)
    funcionario = Funcionario.objects.filter(author=request.user).first()
    expedients = Expedient.objects.filter(departamento=departamento1, recebido=True, estado='Respondido',


                                          )
    page_obj, pagination_range = make_pagination(
        request, expedients, PER_PAGE)

    return render(request,
                  'authors/pages/dashbord_respondidos_funcionario.html', context={
                      'expedients': page_obj,
                      'pagination_range': pagination_range,
                      'funcionario': funcionario

                  }
                  )

# parecer respondido


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_expedient_parecer_responder(request, id, ):

    expedients = Expedient.objects.filter(pk=id).first()
    funcionario = Funcionario.objects.filter(author=request.user).first()
    form = Parecer_Responder_Form(data=request.POST or None,
                                  files=request.FILES or None,
                                  )

    if form.is_valid():
        parecer = form.save(commit=False)
        parecer.tipo = 'Resposta'
        parecer.id_expedient = expedients
        parecer.id_receptor = funcionario.departamento
        parecer.id_emissor = funcionario.departamento
        expedients.estado = 'Respondido'
        #
        # if(tipo=='responder'):
        #   parecer.id_receptor = expedients.
        #  expedients.estado = 'Respondido'
        # else:
        #   expedients.estado = 'Encaminhado'
        expedients.recebido = True
        expedients.save()
        # expedient.estado = 'Novo'
        # expedient.data_emissao = auto_now
       # expedient.numero_Ex = 123
        parecer.save()
        
        try:
            email_user = User.objects.filter(pk=expedients.usuario.id).first()
            print(email_user.email)
            # Enviar e-mail de resposta do expediente
            enviar_email_resposta_expediente(expedients.id, email_user.email, parecer.descricao)
            messages.success(request, 'Expediente respondido com sucesso e e-mail de notificação enviado com sucesso!')
        except Exception as e:
            messages.error(request, f'O expediente foi respondido com sucesso, mas houve um erro ao enviar o e-mail de notificação: {e}')

        return redirect(reverse('authors:dashbord_expedient_recebidos_funcionario'))

    return render(request,
                  'authors/pages/expedient-parecer.html',
                  {
                      'form': form,
                      'form_action': reverse('authors:dashbord_expedient_parecer_responder', args=(id,)),
                      'funcionario': funcionario,
                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_expedient_parecer_encaminhar(request, id, ):

    expedients = Expedient.objects.filter(pk=id).first()
    funcionario = Funcionario.objects.filter(author=request.user).first()
    form = ParecerForm(data=request.POST or None,
                       files=request.FILES or None,
                       )

    if form.is_valid():
        parecer = form.save(commit=False)
        parecer.tipo = 'Encaminhar'
        parecer.id_emissor = funcionario.departamento

        parecer.id_expedient = expedients

        expedients.estado = 'Encaminhado'
        #
        # if(tipo=='responder'):
        #   parecer.id_receptor = expedients.
        #  expedients.estado = 'Respondido'
        # else:
        #   expedients.estado = 'Encaminhado'
        expedients.recebido = True
        expedients.save()
        # expedient.estado = 'Novo'
        # expedient.data_emissao = auto_now
       # expedient.numero_Ex = 123
        parecer.save()
        
        messages.success(request, 'Expediente encaminhado com sucesso!')
        return redirect(reverse('authors:dashbord_expedient_recebidos_funcionario'))

    return render(request,
                  'authors/pages/expedient-parecer.html',
                  {
                      'form': form,
                      'form_action': reverse('authors:dashbord_expedient_parecer_encaminhar', args=(id,)),
                      'funcionario': funcionario,
                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def search(request):
    search_term = request.GET.get('search', '').strip()

    if not search_term:
        raise Http404()

    id_departamento = Funcionario.objects.filter(author=request.user).first()

    # ver_funcionario = Funcionario.objects.filter(author=request.user).first()
    print(id_departamento)
    if id_departamento:
        departamento1 = id_departamento.departamento
        expedients = Expedient.objects.filter(
            Q(

                Q(assunto__contains=search_term) |
                Q(descricao__icontains=search_term),

            ),
            departamento=departamento1,

        ).order_by('-id')
    else:
        expedients = Expedient.objects.filter(
            Q(
                Q(assunto__contains=search_term) |
                Q(descricao__icontains=search_term),
            ),
            usuario=request.user,

        ).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request, expedients, PER_PAGE)

    # recipes = recipes.filter(is_published=True)
   # recipe = Recipe.objects.filter(id=id, is_published=True).order_by('-id').first
    return render(request, 'authors/pages/search.html',
                  context={
                           'page_title': f'Search for "{search_term}"',
                      'search_term': search_term,
                      'expedients': page_obj,
                      'pagination_range': pagination_range,
                      'additional_url_query': f'&search={search_term}',
                      'funcionario': id_departamento,
                  })

# adicionar o funcionario para todas as views!!!
@login_required(login_url='authors:login', redirect_field_name='next')
def secretaria_search(request):
    search_term = request.GET.get('search', '').strip()

    # Obtém o objeto Funcionario associado ao usuário logado
    funcionario = Funcionario.objects.filter(author=request.user).first()

    # Verifica se o Funcionario pertence ao Departamento com o nome "Secretaria"
    if funcionario.departamento.nome == 'Secretaria':
        # Filtra os expedientes com base no formulário de filtro
        filtro = Expedient_filter(request.GET, queryset=Expedient.objects.all())
        expedients = filtro.qs
    else:
        # Caso o Funcionario não pertença ao Departamento "Secretaria", exibe um erro 404
        raise Http404()

    return render(request, 'authors/pages/secretaria_search.html', {
        'funcionario': funcionario,
        'filtro': filtro,
        'expedients': expedients,
    })
'''
@login_required(login_url='authors:login', redirect_field_name='next')
def secretaria_search(request):
    search_term = request.GET.get('search', '').strip()
    #form = AuthorExpedientFormFilter(request.GET)

    id_departamento = Funcionario.objects.filter(author=request.user).first()

    #ver_funcionario = Funcionario.objects.filter(author=request.user).first()
    print(id_departamento.departamento.id)

    if id_departamento.departamento.id == 2:
        expedients = Expedient_filter(
            request.GET, queryset=Expedient.objects.all())
    else:
        raise Http404()

    # page_obj, pagination_range = make_pagination(
    # request, expedients, PER_PAGE)
    filtro = Expedient_filter(request.GET, queryset=Expedient.objects.all())
    # recipes = recipes.filter(is_published=True)
    #recipe = Recipe.objects.filter(id=id, is_published=True).order_by('-id').first
    return render(request, 'authors/pages/secretaria_search.html',
                  context={
                      # 'page_title': f'Search for "{search_term}"',
                      # 'search_term': search_term,
                      # 'expedients': page_obj,
                      # 'pagination_range': pagination_range,
                      # 'additional_url_query': f'&search={search_term}',
                      'funcionario': id_departamento,
                      'filtro': filtro,
                      # 'form': form,
                      'expedients': expedients,

                  })
'''

'''


def secretaria_search(request):
    filtro = Expedient_filter(request.GET, queryset=Expedient.objects.all())
    return render(request, 'authors/pages/secretaria_search.html', {'filtro': filtro})
'''


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_protocol_new(request,):
    funcionario = Funcionario.objects.filter(author=request.user).first()
    if not funcionario:
        raise Http404()
    form = AuthorProtocolForm(data=request.POST or None,
                              files=request.FILES or None,
                              )

    if form.is_valid():
        protocol = form.save(commit=False)
        protocol.estado = 'Pendente'
        protocol.remetente = funcionario
        protocol.save()
        departamento = protocol.destinatario
        #expedient.usuario = request.user
        #expedient.estado = 'Novo'
        # expedient.data_emissao = auto_now
        #expedient.numero_Ex = 123
        # expedient.save()
        # Obtendo todos os funcionários associados ao departamento
        try:
            funcionarios_departamento = Funcionario.objects.filter(departamento=departamento)

                # Obtendo os endereços de e-mail dos funcionários
            destinatarios_email = [funcionario.author.email for funcionario in funcionarios_departamento]

                # Chamando a função para enviar e-mail
            print(destinatarios_email, protocol.id)
            enviar_email_novo_protocolo(protocol.id, destinatarios_email)
            
        except Exception as e:
            # Lidar com outras exceções não tratadas
            print(f"Erro ao enviar e-mail: {str(e)}")
            messages.error(request, 'E-mail não enviado, verifique os dados!')
        
        messages.success(request, 'Protocolo salvo com sucesso!')
        return redirect(reverse('authors:dashbord_protocol_emitidos'))

    return render(request,
                  'authors/pages/dashbord_protocol.html',
                  {
                      'form': form,
                      'funcionario': funcionario,
                      'form_action': reverse('authors:dashbord_protocol_new')
                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_protocol_emitidos(request):
    id_departamento = Funcionario.objects.filter(author=request.user).first()
    departamento = id_departamento.departamento
    print(departamento)
    protocols = Protocolo.objects.filter(remetente=id_departamento,

                                         )
    funcionario = Funcionario.objects.filter(author=request.user).first()
    if not funcionario:
        raise Http404()
    page_obj, pagination_range = make_pagination(
        request, protocols, PER_PAGE)

    return render(request,
                  'authors/pages/dashbord_protocol_emitidos.html', context={
                      'protocols': page_obj,
                      'pagination_range': pagination_range,
                      'funcionario': funcionario,

                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_protocol_emitidos_pendente(request):
    id_departamento = Funcionario.objects.filter(author=request.user).first()
    departamento = id_departamento.departamento
    print(id_departamento.id)
    protocols = Protocolo.objects.filter(estado='Pendente', remetente=id_departamento,

                                         )
    funcionario = Funcionario.objects.filter(author=request.user).first()
    if not funcionario:
        raise Http404()
    page_obj, pagination_range = make_pagination(
        request, protocols, PER_PAGE)

    return render(request,
                  'authors/pages/dashbord_protocol_emitidos.html', context={
                      'protocols': page_obj,
                      'pagination_range': pagination_range,
                      'funcionario': funcionario,

                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_protocol_emitidos_finalizado(request):
    id_departamento = Funcionario.objects.filter(author=request.user).first()
    departamento = id_departamento.departamento
    print(departamento)
    protocols = Protocolo.objects.filter(estado='Finalizado', remetente=id_departamento,
                                         confirmacao_user_status=True,
                                         )
    funcionario = Funcionario.objects.filter(author=request.user).first()
    if not funcionario:
        raise Http404()
    page_obj, pagination_range = make_pagination(
        request, protocols, PER_PAGE)

    return render(request,
                  'authors/pages/dashbord_protocol_emitidos.html', context={
                      'protocols': page_obj,
                      'pagination_range': pagination_range,
                      'funcionario': funcionario,

                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_protocol_recebidos(request):
    id_departamento = Funcionario.objects.filter(author=request.user).first()
    print(id_departamento.id)
    departamento = id_departamento.departamento
    print(departamento)
    protocols = Protocolo.objects.filter(estado='Pendente',
                                         destinatario=departamento,
                                         confirmacao_user_status=False,
                                         )
    funcionario = Funcionario.objects.filter(author=request.user).first()
    if not funcionario:
        raise Http404()
    page_obj, pagination_range = make_pagination(
        request, protocols, PER_PAGE)

    return render(request,
                  'authors/pages/dashbord_protocol_recebidos.html', context={
                      'protocols': page_obj,
                      'pagination_range': pagination_range,
                      'funcionario': funcionario,

                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_protocol_detail(request, id):
    protocol = Protocolo.objects.filter(
        pk=id
    ).first()
    if not protocol:
        raise Http404()

    usuario = protocol.remetente
    print(usuario)
    #id_departamento = Funcionario.objects.filter(author=request.user).first()
    if not protocol:
        raise Http404()
    # print(id_departamento.departamento)

    #parecer = Parecer.objects.filter(id_expedient=id)
    #profile = Profile.objects.filter(author=usuario).first()
    funcionario = Funcionario.objects.filter(author=request.user).first()
    if not funcionario:
        raise Http404()
    #funcionario_expedient = Funcionario.objects.filter(author=usuario).first()
    return render(request,
                  'authors/pages/protocol-detail.html',
                  context={'protocol': protocol,
                           'funcionario': funcionario, }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord_protocol_confirmacao(request, id):
    funcionario = Funcionario.objects.filter(author=request.user).first()
    if not funcionario:
        raise Http404()
    protocol = Protocolo.objects.filter(
        pk=id
    ).first()

    if not protocol:
        raise Http404()
    print(funcionario.id)
    #protocol = form.save(commit=False)
    protocol.estado = 'Finalizado'
    protocol.data_confirmacao_recepcao = timezone.now()
    protocol.confirmacao_user_status = True
    protocol.confirmacao_user = funcionario
    protocol.save()
    #remetente = protocol.remetente
    try:
        remetente_email = protocol.remetente.author.email
        
            # Chamando a função para enviar e-mail
        print(remetente_email, protocol.id)
        enviar_email_protocolo_confirmado(protocol.id, [remetente_email])
        
    except Exception as e:
        # Lidar com outras exceções não tratadas
        print(f"Erro ao enviar e-mail: {str(e)}")
        messages.error(request, 'E-mail não enviado, verifique os dados!')
    # if form.is_valid():
    messages.success(request, 'Protocolo confirmado com sucesso!')
    return redirect(reverse('authors:dashbord_protocol_recebidos'))
    #usuario = expedient.usuario
    # print(usuario)
    #profile = Profile.objects.filter(author=usuario).first()
    #funcionario_expedient = Funcionario.objects.filter(author=usuario).first()
    return render(request,
                  'authors/pages/dashbord_protocol_recebidos.html',
                  {
                      'funcionario': funcionario,
                      'form_action': reverse('authors:dashbord_protocol_confirmacao',  args=(id,))
                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def protocol_search(request):
    #search_term = request.GET.get('search', '').strip()
    #form = AuthorExpedientFormFilter(request.GET)

    id_departamento = Funcionario.objects.filter(author=request.user).first()
    if not id_departamento:
        raise Http404()
    #ver_funcionario = Funcionario.objects.filter(author=request.user).first()
    print(id_departamento.departamento.id)

    if id_departamento:
        protocols = Protocol_filter(
            request.GET, queryset=Protocolo.objects.all())
    else:
        raise Http404()

    # page_obj, pagination_range = make_pagination(
    # request, expedients, PER_PAGE)
    filtro = Protocol_filter(request.GET, queryset=Protocolo.objects.all())
    # recipes = recipes.filter(is_published=True)
    #recipe = Recipe.objects.filter(id=id, is_published=True).order_by('-id').first
    return render(request, 'authors/pages/protocol_search.html',
                  context={
                      # 'page_title': f'Search for "{search_term}"',
                      # 'search_term': search_term,
                       #'filtro': page_obj,
                       #'pagination_range': pagination_range,
                      # 'additional_url_query': f'&search={search_term}',
                      'funcionario': id_departamento,
                      'filtro': filtro,
                      # 'form': form,
                      'protocols': protocols,

                  })
