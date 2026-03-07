from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Barbero, Cliente, Servicio
from .serializers import (
    BarberoSerializer,
    CitaCreateSerializer,
    CitaResponseSerializer,
    ClienteLoginResponseSerializer,
    ClienteLoginSerializer,
    ClienteRegistroSerializer,
    ClienteSerializer,
    ServicioSerializer,
)
from .services import CitaNotFoundError, CitaService, HorarioNoDisponibleError


class CrearCitaView(APIView):
    """
    Vista para crear una nueva cita de barbería.
    """
    service_class = CitaService

    def post(self, request, *args, **kwargs):
        serializer = CitaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            cita = self.service_class().crear_cita(**serializer.validated_data)
        except CitaNotFoundError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except HorarioNoDisponibleError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        response_payload = CitaResponseSerializer({"msg": "Cita creada", "cita_id": cita.id})
        return Response(response_payload.data, status=status.HTTP_201_CREATED)


class ClientesListView(APIView):
    """
    Vista para listar todos los clientes disponibles.
    """
    def get(self, request):
        clientes = Cliente.objects.all()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)


class BarberosListView(APIView):
    """
    Vista para listar todos los barberos disponibles.
    """
    def get(self, request):
        barberos = Barbero.objects.all()
        serializer = BarberoSerializer(barberos, many=True)
        return Response(serializer.data)


class ServiciosListView(APIView):
    """
    Vista para listar todos los servicios disponibles.
    """
    def get(self, request):
        servicios = Servicio.objects.all()
        serializer = ServicioSerializer(servicios, many=True)
        return Response(serializer.data)


class RegistroClienteView(APIView):
    """
    Vista para registrar un nuevo cliente.
    """
    def post(self, request):
        serializer = ClienteRegistroSerializer(data=request.data)
        if serializer.is_valid():
            cliente = serializer.save()
            return Response(
                {
                    "id": cliente.id, 
                    "nombre": cliente.nombre, 
                    "apellido": cliente.apellido,
                    "celular": cliente.celular,
                    "correo": cliente.correo,
                    "msg": "Cliente registrado exitosamente"
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistroClientePageView(TemplateView):
    template_name = "citas/registro.html"


class LoginClienteView(APIView):
    """
    Vista para iniciar sesión con correo y contraseña.
    """
    def post(self, request):
        serializer = ClienteLoginSerializer(data=request.data)
        if serializer.is_valid():
            correo = serializer.validated_data['correo']
            contraseña = serializer.validated_data['contraseña']
            
            try:
                cliente = Cliente.objects.get(correo=correo)
            except Cliente.DoesNotExist:
                return Response(
                    {"error": "El correo o contraseña son incorrectos"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if not cliente.check_password(contraseña):
                return Response(
                    {"error": "El correo o contraseña son incorrectos"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            response_serializer = ClienteLoginResponseSerializer(cliente)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginClientePageView(TemplateView):
    template_name = "citas/login.html"


class CrearCitaPageView(TemplateView):
    template_name = "citas/crear_cita.html"


class HomeView(TemplateView):
    template_name = "citas/index.html"
