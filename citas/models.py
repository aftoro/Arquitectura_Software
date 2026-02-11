from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)

class Barbero(models.Model):
    nombre = models.CharField(max_length=100)

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()

class Horario(models.Model):
    barbero = models.ForeignKey(Barbero, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    disponible = models.BooleanField(default=True)

class Cita(models.Model):
   cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
   barbero = models.ForeignKey(Barbero, on_delete=models.CASCADE)
   servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
   fecha = models.DateTimeField()
   estado = models.CharField(max_length=20, default="reservada")