from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm, widgets

from core import models


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UpdateUserForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"readonly": True})
            

class EventForm(ModelForm):
    class Meta:
        model = models.Event
        fields = ["title", "event_date", "location", "description"]
        widgets = {
          "description": widgets.Textarea(attrs={'rows':5, 'cols': ''}),
          "event_date": widgets.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        }
