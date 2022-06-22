from threading import local
from django.db import models
from django.contrib.auth.models import *

# Create your models here.


class Evento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, verbose_name='Título')
    descricao = models.TextField(
        blank=True, null=True, verbose_name='Descrição')
    data_evento = models.DateTimeField(verbose_name='Data do evento')
    data_criacao = models.DateTimeField(
        auto_now=True, verbose_name='Data de criação')
    local = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Local do evento')

    class Meta:
        db_table = 'evento'

    def __str__(self):
        return self.titulo

    def get_data_evento(self):
        return self.data_evento.strftime('%x %H:%M Hrs')

    def get_data_input_evento(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')
