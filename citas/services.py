from .models import Cliente, Barbero, Servicio, Horario
from .domain.builders import CitaBuilder
from .infra.factories import NotificationFactory


class CitaNotFoundError(Exception):
    pass


class HorarioNoDisponibleError(Exception):
    pass


class ClienteNotFoundError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass

class CitaService:
    def __init__(self, builder_cls=CitaBuilder, notifier_factory=NotificationFactory):
        self.builder_cls = builder_cls
        self.notifier_factory = notifier_factory

    def crear_cita(self, cliente_id, barbero_id, servicio_id, fecha, tipo="normal"):
        if not cliente_id or not barbero_id or not servicio_id or not fecha:
            raise ValueError("Datos incompletos para crear la cita")

        try:
            cliente = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist as exc:
            raise CitaNotFoundError("Cliente no encontrado") from exc

        try:
            barbero = Barbero.objects.get(id=barbero_id)
        except Barbero.DoesNotExist as exc:
            raise CitaNotFoundError("Barbero no encontrado") from exc

        try:
            servicio = Servicio.objects.get(id=servicio_id)
        except Servicio.DoesNotExist as exc:
            raise CitaNotFoundError("Servicio no encontrado") from exc

        if Horario.objects.filter(barbero=barbero, fecha=fecha, disponible=False).exists():
            raise HorarioNoDisponibleError("Horario no disponible")

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
        cita = self.crear_cita(
            cliente_id=payload.get("cliente_id"),
            barbero_id=payload.get("barbero_id"),
            servicio_id=payload.get("servicio_id"),
            fecha=payload.get("fecha"),
            tipo=payload.get("tipo", tipo),
        )
        return {"msg": "Cita creada", "cita_id": cita.id}

    def login_cliente(self, correo, contraseña):
        """Autentica un cliente con correo y contraseña"""
        if not correo or not contraseña:
            raise ValueError("Correo y contraseña son requeridos")

        try:
            cliente = Cliente.objects.get(correo=correo)
        except Cliente.DoesNotExist as exc:
            raise InvalidCredentialsError("El correo o contraseña son incorrectos") from exc

        if not cliente.check_password(contraseña):
            raise InvalidCredentialsError("El correo o contraseña son incorrectos")

        return cliente

    def registro_cliente(self, nombre, apellido, celular, correo, contraseña):
        """Registra un nuevo cliente"""
        if not nombre or not correo or not contraseña:
            raise ValueError("Nombre, correo y contraseña son requeridos")

        if len(contraseña) < 6:
            raise ValueError("La contraseña debe tener minimo 6 caracteres")

        if Cliente.objects.filter(correo=correo).exists():
            raise ValueError("El correo ya está registrado")

        cliente = Cliente.objects.create(
            nombre=nombre,
            apellido=apellido or "",
            celular=celular or "",
            correo=correo
        )
        cliente.set_password(contraseña)
        cliente.save()
        return cliente