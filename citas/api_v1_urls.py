from django.urls import path

from .views import (
    BarberosListView,
    ClientesListView,
    CrearCitaView,
    LoginClienteView,
    RegistroClienteView,
    ServiciosListView,
)

urlpatterns = [
    path("registro/", RegistroClienteView.as_view(), name="registro_api_v1"),
    path("login/", LoginClienteView.as_view(), name="login_api_v1"),
    path("citas/crear/", CrearCitaView.as_view(), name="crear_cita_v1"),
    path("clientes/", ClientesListView.as_view(), name="clientes_list_v1"),
    path("barberos/", BarberosListView.as_view(), name="barberos_list_v1"),
    path("servicios/", ServiciosListView.as_view(), name="servicios_list_v1"),
]
