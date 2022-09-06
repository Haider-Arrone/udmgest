from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from expedient.models import Expedient, Funcionario, Parecer
from expedient.views import expedient
from utils.expedient.pagination import make_pagination

from authors.forms.expedient_form import AuthorExpedientForm
from authors.forms.parecer_form import ParecerForm
from authors.forms.register_form import RegisterFormProfile
from authors.models import Profile

from .forms import LoginForm, RegisterForm

# Create your views here.
PER_PAGES = 20
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
        
        del(request.session['register_form_data'])
        return redirect(reverse('authors:login'))
    return redirect('authors:register')

def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('authors:dashbord'))
    else:
        form = LoginForm()
        return render(request, 'authors/pages/login.html',{
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
            username=form.cleaned_data.get('username',''),
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
    expedients = Expedient.objects.filter(recebido=False, 
                                         usuario=request.user
                                         )
    
    return render(request,
                  'authors/pages/dashbord.html',
                  {
                      'expedients': expedients
                  }
                  )

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
        #expedient.data_emissao = auto_now
        
        expedient.save()
        
        messages.success(request, 'Expediente salvo com sucesso!')
        return redirect(reverse('authors:dashbord_expedient_edit',args=(id,)))
    
    return render(request,
                  'authors/pages/dashbord_expedient.html',
                  {
                  'form': form    
                  }
                  )
   
   
    
@login_required(login_url='authors:login', redirect_field_name='next')    
def dashbord_expedient_new(request,):
    
    form = AuthorExpedientForm(data=request.POST or None,
                               files=request.FILES or None,
                               )
    
    if form.is_valid():
        expedient = form.save(commit=False)
        
        expedient.usuario = request.user
        expedient.estado = 'Novo'
        #expedient.data_emissao = auto_now
        expedient.numero_Ex = 123
        expedient.save()
        
        messages.success(request, 'Expediente salvo com sucesso!')
        return redirect(reverse('authors:dashbord'))
    
    return render(request,
                  'authors/pages/dashbord_expedient.html',
                  {
                  'form': form,
                  'form_action':reverse('authors:dashbord_expedient_new')    
                  }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')    
def dashbord_expedient_emitidos(request):
    expedients = Expedient.objects.filter(recebido=False, 
                                         usuario=request.user,
                                        
                                         )
    page_obj, pagination_range = make_pagination(request, expedients, PER_PAGES)
    
    return render(request,
                  'authors/pages/dashbord_emitidos.html',context={
        'expedients': page_obj,
        'pagination_range': pagination_range,
       
    }
                  )


@login_required(login_url='authors:login', redirect_field_name='next')    
def dashbord_expedient_recebidos(request):
    expedients = Expedient.objects.filter(recebido=True, estado='Respondido',
                                         usuario=request.user,
                                        
                                         )
    page_obj, pagination_range = make_pagination(request, expedients, PER_PAGES)
    
    return render(request,
                  'authors/pages/dashbord_recebidos.html',context={
        'expedients': page_obj,
        'pagination_range': pagination_range,
       
    }
                  )


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

@login_required(login_url='authors:login', redirect_field_name='next')    
def dashbord_expedient_recebidos_funcionario(request):
    id_departamento = Funcionario.objects.get(author=request.user)
    departamento1 = id_departamento.departamento
    print(departamento1)
    expedients = Expedient.objects.filter(departamento=departamento1, recebido=False, estado='Novo',
                                         
                                        
                                         )
    page_obj, pagination_range = make_pagination(request, expedients, PER_PAGES)
    
    return render(request,
                  'authors/pages/dashbord_recebidos_funcionario.html',context={
        'expedients': page_obj,
        'pagination_range': pagination_range,
       
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
    parecer = Parecer.objects.filter(id_expedient=id)
    
    
    if form.is_valid():
        expedient = form.save(commit=False)
        
        expedient.usuario = request.user
        expedient.estado = 'Novo'
        #expedient.data_emissao = auto_now
        
        expedient.save()
        
        messages.success(request, 'Expediente salvo com sucesso!')
        return redirect(reverse('authors:dashbord_expedient_edit',args=(id,)))                         
    return render(request,
                  'authors/pages/expedient-detail.html',
                  context={'expedient': expedient, 'parecer': parecer,}
                  )

@login_required(login_url='authors:login', redirect_field_name='next')    
def dashbord_expedient_parecer(request, id):
    
    expedients = Expedient.objects.filter(pk=id).first()
                                                                           
    form = ParecerForm(data=request.POST or None,
                               files=request.FILES or None,
                               )
    
    if form.is_valid():
        parecer = form.save(commit=False)
        print(id)
        parecer.id_expedient = expedients
        
        #expedient.estado = 'Novo'
        #expedient.data_emissao = auto_now
       # expedient.numero_Ex = 123
        parecer.save()
        
        messages.success(request, 'Parecer submetido com sucesso!')
        return redirect(reverse('authors:dashbord_expedient_recebidos_funcionario'))
    
    return render(request,
                   'authors/pages/expedient-parecer.html',
                  {
                  'form': form,
                  'form_action':reverse('authors:dashbord_expedient_parecer', args=(id,))    
                  }
                  )
