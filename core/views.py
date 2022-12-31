from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from core.models import *


# Create your views here.
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = UserCreationForm()
    
    data = {"form": form}
    return render(request, "registration/register.html", data)


def logout_user(request):
    logout(request)

    return redirect("/")


@login_required(login_url="/login/")
def get_event_date_by_title(request, titulo_evento):
    try:
        event = Evento.objects.get(titulo=titulo_evento)

        if event.usuario == request.user:
            return HttpResponse(f"{event.data_evento:A data do evento é %x às %X}")
        else:
            raise HttpResponseForbidden()
    except Evento.DoesNotExist:
        raise Http404()


@login_required(login_url="/login/")
def list_events(request):
    event_passed_date = datetime.now() - timedelta(hours=1)
    events = Evento.objects.filter(
        usuario=request.user, data_evento__gt=event_passed_date
    ).order_by("data_evento")
    data = {"eventos": events}

    return render(request, "agenda.html", data)


def list_passed_events(request):
    event_passed_date = datetime.now() - timedelta(hours=1)
    events = Evento.objects.filter(
        usuario=request.user, data_evento__lt=event_passed_date
    ).order_by("data_evento")
    data = {"eventos": events}

    return render(request, "eventos-passados.html", data)


@login_required(login_url="/login/")
def add_update_event(request):
    event_id = request.GET.get("id")
    data = {}

    if event_id:
        data["evento"] = Evento.objects.get(id=event_id)

        if data["evento"].usuario != request.user:
            return redirect("/")

    return render(request, "evento.html", data)


@login_required(login_url="/login/")
def submit_event(request):
    if request.POST:
        event_id = request.POST.get("id")
        user = request.user
        title = request.POST.get("titulo")
        event_location = request.POST.get("local")
        event_date = request.POST.get("data_evento")
        description = request.POST.get("descricao")

        if title == "":
            messages.error(request, "O campo título é obrigatório")

            return redirect("/agenda/evento/")
        try:
            if not event_id:
                Evento.objects.create(
                    usuario=user,
                    titulo=title,
                    data_evento=event_date,
                    local=event_location,
                    descricao=description,
                )
            else:
                event = Evento.objects.get(id=event_id)

                if event.usuario == user:
                    event.titulo = title
                    event.local = event_location
                    event.data_evento = event_date
                    event.descricao = description
                    event.save()
        except ValidationError:
            messages.error(request, "Selecione uma data valida")

            return redirect("/agenda/evento/")

    return redirect("/")


@login_required(login_url="/login/")
def delete_event(request, id_evento):
    try:
        event = Evento.objects.get(id=id_evento)

        if event.usuario == request.user:
            event.delete()
            return redirect("/")
        else:
            raise HttpResponseForbidden()
    except Evento.DoesNotExist:
        raise Http404()


def json_list_events(request, id_usuario):
    user = User.objects.get(id=id_usuario)
    events = Evento.objects.filter(usuario=user).values("id", "titulo")
    return JsonResponse(
        list(events), safe=False, json_dumps_params={"indent": 4, "ensure_ascii": False}
    )
