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
