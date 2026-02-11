from ..models import Cita


class CitaBuilder:
    def __init__(self):
        self._cita = Cita()

    def set_cliente(self, cliente):
        self._cita.cliente = cliente
        return self

    def set_barbero(self, barbero):
        self._cita.barbero = barbero
        return self

    def set_servicio(self, servicio):
        self._cita.servicio = servicio
        return self

    def set_fecha(self, fecha):
        self._cita.fecha = fecha
        return self

    def validate(self):
        if not self._cita.cliente:
            raise ValueError("Cliente requerido")
        if not self._cita.barbero:
            raise ValueError("Barbero requerido")
        if not self._cita.servicio:
            raise ValueError("Servicio requerido")
        if not self._cita.fecha:
            raise ValueError("Fecha requerida")

    def build(self):
        self.validate()
        return self._cita

    def save(self):
        self.validate()
        self._cita.save()
        return self._cita
