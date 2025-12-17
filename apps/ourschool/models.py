from django.db import models
from simple_history.models import HistoricalRecords


class Usuario(models.Model):
    ROLES = (
        (1, "admin"),
        (2, "estudiante"),
        (3, "docente")
    )

    nombre_apellido = models.CharField(max_length=30)
    tipo_documento = models.CharField(max_length=30)
    numero_documento = models.CharField(max_length=30, default=0)
    telefono = models.IntegerField(default=0)
    correo = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField()
    contrasena = models.CharField(max_length=30)
    rol = models.IntegerField(choices=ROLES)

    history = HistoricalRecords()

    def __str__(self):
        return self.nombre_apellido


class Archivo(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='archivos/%Y/%m/%d/')

    history = HistoricalRecords()

    def __str__(self):
        return self.nombre


class Animal(models.Model):
    dueño = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=30)
    nombre = models.CharField(max_length=40)
    foto = models.ImageField(upload_to="ganado/", blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class EventoAnimal(models.Model):
    TIPOS = (
        ("parto", "Parto"),
        ("palpacion", "Palpación"),
        ("destete", "Destete"),
        ("nacimiento", "Nacimiento")
    )

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.animal.nombre} - {self.tipo}"
