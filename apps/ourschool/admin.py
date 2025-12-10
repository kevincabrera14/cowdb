from django.contrib import admin
from .models import Usuario, Archivo, Animal, EventoAnimal
from .models import *
admin.site.register(Usuario)
admin.site.register(Archivo)
admin.site.register(Animal)
admin.site.register(EventoAnimal)

