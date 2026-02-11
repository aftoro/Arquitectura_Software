from django.urls import path
from .views import CrearCitaView

urlpatterns = [
    path("crear/", CrearCitaView.as_view(), name="crear_cita"),
]