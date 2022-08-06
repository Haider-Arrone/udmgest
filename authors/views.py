from django.urls import reverse
from django.shortcuts import render, redirect

from authors.forms.register_form import RegisterFormProfile
from .forms import RegisterForm
from .forms import RegisterForm
from django.http import Http404
from django.contrib import messages
from authors.models import Profile

# Create your views here.
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
        
        messages.success(request, 'Your user is created, log in') 
        
        del(request.session['register_form_data'])
        
    return redirect('authors:register')
