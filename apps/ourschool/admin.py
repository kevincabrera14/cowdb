from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Usuario, Archivo, Animal, EventoAnimal


@admin.register(Usuario)
class UsuarioAdmin(SimpleHistoryAdmin):
    list_display = ("id", "nombre_apellido", "rol")
    search_fields = ("nombre_apellido", "correo")
    list_filter = ("rol",)


@admin.register(Archivo)
class ArchivoAdmin(SimpleHistoryAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


@admin.register(Animal)
class AnimalAdmin(SimpleHistoryAdmin):
    list_display = ("id", "nombre", "codigo", "dueño")
    search_fields = ("nombre", "codigo")
    list_filter = ("dueño",)


@admin.register(EventoAnimal)
class EventoAnimalAdmin(SimpleHistoryAdmin):
    list_display = ("id", "animal", "tipo", "fecha")
    search_fields = ("animal__nombre", "tipo")
    list_filter = ("tipo", "fecha")
