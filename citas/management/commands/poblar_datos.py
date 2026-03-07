from django.core.management.base import BaseCommand
from citas.models import Cliente, Barbero, Servicio, Horario
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Poblar base de datos con datos de prueba'

    def handle(self, *args, **options):
        # Limpiar datos existentes
        Cliente.objects.all().delete()
        Barbero.objects.all().delete()
        Servicio.objects.all().delete()
        Horario.objects.all().delete()

        # Crear clientes
        clientes = [
            Cliente.objects.create(
                nombre="Juan", 
                apellido="Perez", 
                celular="+57 300 123 4567",
                correo="juan@example.com"
            ),
            Cliente.objects.create(
                nombre="Maria", 
                apellido="Lopez", 
                celular="+57 301 234 5678",
                correo="maria@example.com"
            ),
            Cliente.objects.create(
                nombre="Carlos", 
                apellido="Rodriguez", 
                celular="+57 302 345 6789",
                correo="carlos@example.com"
            ),
            Cliente.objects.create(
                nombre="Ana", 
                apellido="Martinez", 
                celular="+57 303 456 7890",
                correo="ana@example.com"
            ),
            Cliente.objects.create(
                nombre="Pedro", 
                apellido="Gonzalez", 
                celular="+57 304 567 8901",
                correo="pedro@example.com"
            ),
        ]
        self.stdout.write(self.style.SUCCESS(f'Creados {len(clientes)} clientes'))

        # Crear barberos
        barberos = [
            Barbero.objects.create(nombre="Nicolas"),
            Barbero.objects.create(nombre="Julian"),
            Barbero.objects.create(nombre="Laura"),
            Barbero.objects.create(nombre="Mateo"),
        ]
        self.stdout.write(self.style.SUCCESS(f'Creados {len(barberos)} barberos'))

        # Crear servicios
        servicios = [
            Servicio.objects.create(nombre="Corte clasico", precio=22000),
            Servicio.objects.create(nombre="Fade", precio=25000),
            Servicio.objects.create(nombre="Barba", precio=18000),
            Servicio.objects.create(nombre="Premium", precio=32000),
        ]
        self.stdout.write(self.style.SUCCESS(f'Creados {len(servicios)} servicios'))

        # Crear horarios disponibles para los próximos días
        today = datetime.now()
        for i in range(1, 15):
            fecha = today + timedelta(days=i)
            for barbero in barberos:
                # Crear horarios disponibles (8am-6pm)
                for hour in range(8, 18, 2):
                    Horario.objects.create(
                        barbero=barbero,
                        fecha=fecha.replace(hour=hour, minute=0, second=0),
                        disponible=True
                    )
        
        self.stdout.write(self.style.SUCCESS('Horarios creados para los próximos 14 días'))
        self.stdout.write(self.style.SUCCESS('Base de datos poblada exitosamente!'))
