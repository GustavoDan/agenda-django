from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import *


# Create your models here.
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='Título')
    description = models.TextField(blank=True, null=True, verbose_name='Descrição')
    event_date = models.DateTimeField(verbose_name='Data do evento')
    creation_date = models.DateTimeField(auto_now=True, verbose_name='Data de criação')
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name='Local do evento')

    class Meta:
        db_table = 'event'

    def __str__(self):
        return self.title

    def get_event_date(self):
        return self.event_date.strftime('%x %H:%M Hrs')

    def has_passed(self):
        return self.event_date < datetime.now() and self.event_date > datetime.now() - timedelta(hours=1)

    def will_happen_soon(self):
        return self.event_date < datetime.now() + timedelta(hours=1) and self.event_date > datetime.now()
