from django import forms
from .models import Archivo
from .models import EventoAnimal


class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ['nombre', 'archivo']



class EventoForm(forms.ModelForm):
    class Meta:
        model = EventoAnimal
        fields = ["tipo", "fecha", "descripcion"]
