from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Barbero, Cita, Cliente, Horario, Servicio


class CrearCitaApiTests(APITestCase):
	def setUp(self):
		self.url = reverse("crear_cita")
		self.cliente = Cliente.objects.create(nombre="Juan")
		self.barbero = Barbero.objects.create(nombre="Pedro")
		self.servicio = Servicio.objects.create(nombre="Corte", precio=20)
		self.fecha = "2030-01-01T10:00:00Z"

	def test_crear_cita_retorna_201(self):
		payload = {
			"cliente_id": self.cliente.id,
			"barbero_id": self.barbero.id,
			"servicio_id": self.servicio.id,
			"fecha": self.fecha,
			"tipo": "normal",
		}

		response = self.client.post(self.url, payload, format="json")

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Cita.objects.count(), 1)
		self.assertIn("cita_id", response.data)

	def test_crear_cita_payload_invalido_retorna_400(self):
		payload = {
			"cliente_id": self.cliente.id,
			"barbero_id": self.barbero.id,
			"tipo": "normal",
		}

		response = self.client.post(self.url, payload, format="json")

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_crear_cita_recurso_no_encontrado_retorna_404(self):
		payload = {
			"cliente_id": 99999,
			"barbero_id": self.barbero.id,
			"servicio_id": self.servicio.id,
			"fecha": self.fecha,
			"tipo": "normal",
		}

		response = self.client.post(self.url, payload, format="json")

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_crear_cita_conflicto_retorna_409(self):
		Horario.objects.create(
			barbero=self.barbero,
			fecha="2030-01-01T10:00:00Z",
			disponible=False,
		)
		payload = {
			"cliente_id": self.cliente.id,
			"barbero_id": self.barbero.id,
			"servicio_id": self.servicio.id,
			"fecha": self.fecha,
			"tipo": "normal",
		}

		response = self.client.post(self.url, payload, format="json")

		self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
