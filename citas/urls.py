from django.urls import path
from .views import (
    BarberosListView,
    ClientesListView,
    CrearCitaPageView,
    CrearCitaView,
    HomeView,
    LoginClientePageView,
    LoginClienteView,
    RegistroClientePageView,
    RegistroClienteView,
    ServiciosListView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("registro/", RegistroClientePageView.as_view(), name="registro_page"),
    path("login/", LoginClientePageView.as_view(), name="login_page"),
    path("crear/", CrearCitaPageView.as_view(), name="crear_cita_page"),
    path("api/registro/", RegistroClienteView.as_view(), name="registro_api"),
    path("api/login/", LoginClienteView.as_view(), name="login_api"),
    path("api/citas/crear/", CrearCitaView.as_view(), name="crear_cita"),
    path("api/clientes/", ClientesListView.as_view(), name="clientes_list"),
    path("api/barberos/", BarberosListView.as_view(), name="barberos_list"),
    path("api/servicios/", ServiciosListView.as_view(), name="servicios_list"),
]