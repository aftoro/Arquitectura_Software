from .models import Cita, Horario
from .builders import CitaBuilder
from .factories import CitaFactory

class CitaService:

    @staticmethod
    def crear_cita(cliente, barbero, servicio, fecha, tipo="normal"):
        if Horario.objects.filter(barbero=barbero, fecha=fecha, disponble=False).exists():
            raise Exception("Horario no disponible :(")
        
        builder = CitaBuilder()
        cita = (builder
                .set_cliente(cliente)
                .set_barbero(barbero)
                .set_servicio(servicio)
                .set_fecha(fecha)
                .save())
        
        cita = CitaFactory.crear_cita(tipo, cita)
        
        return cita