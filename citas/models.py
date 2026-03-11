from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
import re

def validate_celular(value):
    """Valida que el formato del celular sea válido (10-20 caracteres)"""
    if value and len(value) < 10:
        raise ValidationError("El celular debe tener al menos 10 caracteres")
    if value and len(value) > 20:
        raise ValidationError("El celular no puede exceder 20 caracteres")
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, default="")
    celular = models.CharField(max_length=20, blank=True, default="", validators=[validate_celular])
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
    
    def clean(self):
        if self.precio <= 0:
            raise ValidationError("El precio debe ser mayor a 0")

class Horario(models.Model):
    barbero = models.ForeignKey(Barbero, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    disponible = models.BooleanField(default=True)
    
    def clean(self):
        from datetime import datetime
        if self.fecha < datetime.now():
            raise ValidationError("La fecha no puede ser anterior a hoy")

class Cita(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    barbero = models.ForeignKey(Barbero, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=20, default="reservada")
    
    def clean(self):
        from datetime import datetime
        if self.fecha < datetime.now():
            raise ValidationError("La fecha de la cita no puede ser anterior a hoy")
        if self.estado not in ["reservada", "cancelada", "completada"]:
            raise ValidationError("Estado de cita inválido")
    
    def __str__(self):
        return f"Cita de {self.cliente.nombre} - {self.fecha}"