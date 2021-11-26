from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Equipo.views import equipos,equipo
from Jugador.views import jugadores,jugador
from Scraping import views
from Liga.views import ligas,tabla, maximosEstadisticas
from Estadisticas.views import estadisticasJugador,notasJugador,caracteristicasJugador

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.cargar),
    path('liga/<int:id_liga>', ligas.as_view(), name="Liga"),
    path('liga/tabla/<int:id_liga>', tabla.as_view(), name="Tabla"),
    path('liga/maximos/<int:id_liga>', maximosEstadisticas.as_view(), name="Maximos"),
    path('equipo/todos/<int:id_liga>', equipos.as_view(),name="Equipos"),
    path('equipo/<int:id_equipo>', equipo.as_view(),name="Equipo"),
    path('jugador/todos/<int:id_equipo>',jugadores.as_view(), name="Jugadores"),
    path('jugador/<int:id_jugador>',jugador.as_view(), name="Jugador"),
    path('jugador/estadisticas/<int:id_jugador>', estadisticasJugador.as_view(), name="estadisticas"),
    path('jugador/notas/<int:id_jugador>', notasJugador.as_view(), name="notas"),
    path('jugador/caracteristicas/<int:id_jugador>', caracteristicasJugador.as_view(), name="caracteristicas"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
