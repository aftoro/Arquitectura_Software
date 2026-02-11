from django.http import JsonResponse
from .models import Cliente, Barbero, Servicio, Horario
from .domain.builders import CitaBuilder
from .infra.factories import NotificationFactory

class CitaService:
    def __init__(self, builder_cls=CitaBuilder, notifier_factory=NotificationFactory):
        self.builder_cls = builder_cls
        self.notifier_factory = notifier_factory

    def crear_cita(self, cliente_id, barbero_id, servicio_id, fecha, tipo="normal"):
        cliente = Cliente.objects.get(id=cliente_id)
        barbero = Barbero.objects.get(id=barbero_id)
        servicio = Servicio.objects.get(id=servicio_id)

        if Horario.objects.filter(barbero=barbero, fecha=fecha, disponible=False).exists():
            raise Exception("Horario no disponible :(")

        builder = self.builder_cls()
        cita = (builder
                .set_cliente(cliente)
                .set_barbero(barbero)
                .set_servicio(servicio)
                .set_fecha(fecha)
                .save())

        notifier = self.notifier_factory.get_notifier()
        notifier.send(cliente.nombre, "Cita creada", f"Tipo: {tipo}")

        return cita

    def crear_cita_response(self, payload, tipo="premium"):
        try:
            cita = self.crear_cita(
                cliente_id=payload.get("cliente_id"),
                barbero_id=payload.get("barbero_id"),
                servicio_id=payload.get("servicio_id"),
                fecha=payload.get("fecha"),
                tipo=tipo,
            )
            return JsonResponse({"msg": "Cita creada", "cita_id": cita.id})
        except Exception as exc:
            return JsonResponse({"error": str(exc)}, status=400)