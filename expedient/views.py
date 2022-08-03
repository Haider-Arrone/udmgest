from django.shortcuts import render

from utils.expedient.pagination import make_pagination
from .models import Expedient
from django.core.paginator import Paginator

PER_PAGES = 20

def home(request):
    expedients = Expedient.objects.filter(recebido=False).order_by('-id')
    
    page_obj, pagination_range = make_pagination(request, expedients, PER_PAGES)
    
    return render(request, 'expedient/pages/home.html', context={
        'expedients': page_obj,
        'pagination_range': pagination_range,
       
    })

def expedient(request, id):
    expedient = Expedient.objects.filter(id=id).order_by('-id').first
    return render(request, 'expedient/pages/expedient-view.html', context={
        'expedient': expedient(),
        
    })
