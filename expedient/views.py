import os

from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from utils.expedient.pagination import make_pagination

from .models import Expedient

PER_PAGE = int(os.environ.get('PER_PAGE', 10))


def home(request):
    return redirect(reverse('authors:dashbord'))


def expedient(request, id):
    expedient = Expedient.objects.filter(id=id).order_by('-id').first
    return render(request, 'expedient/pages/expedient-view.html', context={
        'expedient': expedient(),

    })
