from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.forms.models import model_to_dict

from core import forms
from core import models


class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy("user")
    template_name = "user/change-password.html"

    def form_valid(self, form):
        messages.success(self.request, "Sua senha foi modificada com sucesso!!!")
        return super().form_valid(form)


# Create your views here.
def register_user(request):
    if request.user.is_authenticated:
        return redirect("root")

    form = forms.RegisterUserForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()

        username = form.cleaned_data.get("username")
        messages.success(request, f"Usuário {username} criado com sucesso!!!")
        return redirect("login")

    data = {"form": form}
    return render(request, "user/register.html", data)


@login_required()
def logout_user(request):
    logout(request)
    return redirect("root")


@login_required()
def user_page(request):
    user = request.user
    form = forms.UpdateUserForm(request.POST or None, instance=user)

    if request.method == "POST":
        old_user_data = model_to_dict(user)
        
        if form.is_valid():
            if model_to_dict(user) != old_user_data: 
                form.save()
                messages.success(request, "Perfil atualizado com sucesso!!!")
            
            return redirect("user")
        else:
            form.data = old_user_data
            user.username = old_user_data.get("username")
        
    data = {"form": form}
    return render(request, "user/profile.html", data)


@login_required()
def list_events(request):
    event_passed_date = datetime.now() - timedelta(hours=1)
    events = models.Event.objects.filter(user=request.user, event_date__gt=event_passed_date).order_by("event_date")
    
    data = {"events": events}
    return render(request, "schedules.html", data)


@login_required()
def list_passed_events(request):
    event_passed_date = datetime.now() - timedelta(hours=1)
    events = models.Event.objects.filter(user=request.user, event_date__lt=event_passed_date).order_by("event_date")

    data = {"events": events}
    return render(request, "past-schedules.html", data)


@login_required()
def create_or_update_event(request):
    event_id = request.GET.get("id")
    event = None
    
    try:
        if event_id:
            event = models.Event.objects.get(id=event_id)
    except models.Event.DoesNotExist:
        return HttpResponseNotFound()
    
    form = forms.EventForm(request.POST or None, instance=event)
    if event is not None and event.user != request.user:
        return HttpResponseForbidden()
            
    if request.method == "POST" and form.is_valid():
        event = form.save(commit=False)
        event.user = request.user
        event.save()
        messages.success(request, f"Evento {'atualizado' if event_id else 'adicionado'} com sucesso!!!")
        
        return redirect("root")
    
    data = {"form": form}
    return render(request, "event.html", data)


@login_required()
def delete_event(request, event_id):
    try:
        event = models.Event.objects.get(id=event_id)

        if event.user == request.user:
            event.delete()
            messages.success(request, "Evento deletado com sucesso!!!")
            
            return redirect("root")
        else:
            return HttpResponseForbidden()
    except models.Evento.DoesNotExist:
        return HttpResponseNotFound()


def json_list_events(request, user_id):
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return HttpResponseNotFound()
    
    events = models.Event.objects.filter(user=user).values("id", "title")
    return JsonResponse(
        list(events), safe=False, json_dumps_params={"indent": 4, "ensure_ascii": False}
    )
