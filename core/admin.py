from django.contrib import admin
from core.models import *


class EventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'data_evento', 'data_criacao')
    list_filter = ('usuario', 'data_evento')


# Register your models here.
admin.site.register(Evento, EventoAdmin)
