from django.views.generic import TemplateView
from .services import CitaService

class CrearCitaView(TemplateView):
    template_name = "citas/crear_cita.html"
    service_class = CitaService

    def post(self, request, *args, **kwargs):
        return self.service_class().crear_cita_response(request.POST)


class HomeView(TemplateView):
    template_name = "citas/index.html"
