from django.contrib import admin
from .models import Usuario, Archivo, Animal, EventoAnimal
from .models import *
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Animal, EventoAnimal

admin.site.register(Usuario)
admin.site.register(Archivo)
admin.site.register(Animal)
admin.site.register(EventoAnimal)


