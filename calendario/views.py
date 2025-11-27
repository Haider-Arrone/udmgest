from django.shortcuts import render
from .models import Event
from calendario.forms.evento_form import EventForm 
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import json
from django.http import JsonResponse
from datetime import timedelta
# Create your views here.
def calendar_view(request):
    return render(request, "calendario/calendar.html")

def calendar_interno_view(request):
    return render(request, "calendario/calendar_interno.html")

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


def event_list_api(request):
    events = Event.objects.all()
    data = []

    for event in events:
        if event.start_date and event.end_date:
            current_date = event.start_date
            while current_date <= event.end_date:
                if current_date.weekday() != 6:  # 6 = domingo
                    data.append({
                        "title": event.title,
                        "start": str(current_date),
                        "type": event.type,
                        "semester": event.semester,
                        "course": event.course,
                        "turma": event.turma,
                        "color": event.color, 
                    })
                current_date += timedelta(days=1)
        else:
            # caso o evento não tenha datas, ainda podemos adicioná-lo
            data.append({
                "title": event.title,
                "start": str(event.start_date) if event.start_date else None,
                "type": event.type,
                "semester": event.semester,
                "course": event.course,
                "turma": event.turma,
                "color": event.color, 
            })

    return JsonResponse(data, safe=False)