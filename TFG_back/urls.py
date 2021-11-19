"""TFG_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Scraping import views
from Estadisticas.views import estadisticasJugador,notasJugador,caracteristicasJugador
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.cargar),
    path('jugador/estadisticas/<int:id_jugador>', estadisticasJugador.as_view(), name="estadisticas"),
    path('jugador/notas/<int:id_jugador>', notasJugador.as_view(), name="notas"),
    path('jugador/caracteristicas/<int:id_jugador>', caracteristicasJugador.as_view(), name="caracteristicas"),
]
