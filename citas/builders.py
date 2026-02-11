from .models import Cita

class CitaBuilder:
    def __init__(self):
        self.cita = Cita()

    def set_cliente(self, cliente):
        self.cita.cliente = cliente
        return self

    def set_barbero(self, barbero):
        self.cita.barbero = barbero
        return self

    def set_servicio(self, servicio):
        self.cita.servicio = servicio
        return self

    def set_fecha(self, fecha):
        self.cita.fecha = fecha
        return self

    def validate(self):
        if not self.cita.cliente:
            raise ValueError("Cliente requerido")
        if not self.cita.fecha:
            raise ValueError("Fecha requerida")

    def save(self):
        self.validate()
        self.cita.save()
        return self.cita
