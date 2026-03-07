from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, default="")
    celular = models.CharField(max_length=20, blank=True, default="")
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255, default="")
    
    def set_password(self, raw_password):
        self.contraseña = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.contraseña)

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