from django.shortcuts import render
from .models import Expedient

def home(request):
    expedients = Expedient.objects.filter(recebido=False).order_by('-id')
    
    #page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)
    
    return render(request, 'expedient/pages/home.html', context={
        'expedients': expedients,
    #    'pagination_range': pagination_range,
       
    })
