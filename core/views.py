from django.shortcuts import render, HttpResponse
from core.models import *


# Create your views here.
def get_event_date_by_title(request, titulo_evento):
    return HttpResponse(f'{Evento.objects.get(titulo=titulo_evento).data_evento:A data do evento é %x às %X}')