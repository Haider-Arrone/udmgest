from django.shortcuts import render
from .models import Event
from calendario.forms.evento_form import EventForm 
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import json
# Create your views here.
def calendar_view(request):
    return render(request, "calendario/calendar.html")

# Lista de eventos
def event_list(request):
    events = Event.objects.all()
    events_list = []
    for event in events:
        events_list.append({
            'title': event.title,
            'start': event.date.isoformat(),
            'className': f'event-{event.type}'  # para cores por tipo
        })
    # converte para JSON
    events_json = json.dumps(events_list)
    return render(request, 'calendario/list_calendario.html', {'events': events_json})

# Criar novo evento
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event-list')
    else:
        form = EventForm()
    return render(request, 'calendario/criar_calendario.html', {'form': form})