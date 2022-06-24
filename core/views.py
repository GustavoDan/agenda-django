from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
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
    event_passed_date = datetime.now() - timedelta(hours=1)
    events = Evento.objects.filter(usuario=user,
                                   data_evento__gt=event_passed_date)
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

        if not event_id:
            Evento.objects.create(usuario=user,
                                  titulo=title,
                                  data_evento=event_date,
                                  local=event_location,
                                  descricao=description)
        else:
            # Evento.objects.filter(id=event_id).update(titulo=title,
            #                                          data_evento=event_date,
            #                                          local=event_location,
            #                                          descricao=description)
            event = Evento.objects.get(id=event_id)

            if event.usuario == user:
                event.titulo = title
                event.local = event_location
                event.data_evento = event_date
                event.descricao = description
                event.save()

    return redirect('/')


@login_required(login_url='/login/')
def delete_event(request, id_evento):
    user = request.user

    try:
        event = Evento.objects.get(id=id_evento)
    except Evento.DoesNotExist:
        raise Http404()

    if event.usuario == user:
        event.delete()
        return redirect('/')
    else:
        raise Http404()


def json_list_events(request, id_usuario):
    user = User.objects.get(id=id_usuario)
    events = Evento.objects.filter(usuario=user).values('id', 'titulo')
    return JsonResponse(list(events), safe=False, json_dumps_params={'indent': 4, 'ensure_ascii': False})
