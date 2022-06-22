from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse
from core.models import *

# Create your views here.
# def index(request):
#     return redirect('agenda/')


def login_user(request):
    return render(request, 'login.html')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            messages.error(request, "Usuário ou senha inválidos")

    return redirect('/')


def logout_user(request):
    logout(request)

    return redirect('/')


def get_event_date_by_title(request, titulo_evento):
    return HttpResponse(f'{Evento.objects.get(titulo=titulo_evento).data_evento:A data do evento é %x às %X}')


@login_required(login_url='/login/')
def list_events(request):
    user = request.user
    events = Evento.objects.filter(usuario=user)
    response = {'eventos': events}

    return render(request, 'agenda.html', response)


@login_required(login_url='/login/')
def add_update_event(request):
    event_id = request.GET.get('id')
    data = {}

    if event_id:
        data['evento'] = Evento.objects.get(id=event_id)

        if data['evento'].usuario != request.user:
            return redirect('/')

    return render(request, 'evento.html', data)


@login_required(login_url='/login/')
def submit_event(request):
    if request.POST:
        event_id = request.POST.get('id')
        user = request.user
        title = request.POST.get('titulo')
        event_location = request.POST.get('local')
        event_date = request.POST.get('data_evento')
        description = request.POST.get('descricao')

        if event_id is None:
            Evento.objects.create(usuario=user,
                                  titulo=title,
                                  data_evento=event_date,
                                  local=event_location,
                                  descricao=description)
        else:
            event = Evento.objects.get(event_id=event_id)

            if event.usuario == user:
                event.update(titulo=title,
                             data_evento=event_date,
                             local=event_location,
                             descricao=description)
                # event.titulo = title
                # event.local=event_location
                # event.data_evento=event_date
                # event.descricao=description
                # event.save()

    return redirect('/')


@login_required(login_url='/login/')
def delete_event(request, id_evento):
    user = request.user
    event = Evento.objects.get(id=id_evento)

    if event.usuario == user:
        event.delete()

    return redirect('/')
