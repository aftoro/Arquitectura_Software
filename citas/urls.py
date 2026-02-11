from django.urls import path
from .views import CrearCitaView, HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("crear/", CrearCitaView.as_view(), name="crear_cita"),
]