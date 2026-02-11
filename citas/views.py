from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .services import CitaService
from .models import Cliente, Barbero, Servicio

class CrearCitaView(View):

    def post(self, request):
        cliente_id = request.POST.get("cliente_id")
        barbero_id = request.POST.get("barbero_id")
        servicio_id = request.POST.get("servicio_id")
        fecha = request.POST.get("fecha")
     
        cliente = Cliente.objects.get(id=cliente_id)
        barbero = Barbero.objects.get(id=barbero_id)
        servicio = Servicio.objects.get(id=servicio_id)

        try:
            cita = CitaService.crear_cita(cliente, barbero, servicio, fecha, tipo="premium")
            return JsonResponse({"msg": "Cita creada", "cita_id": cita.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
