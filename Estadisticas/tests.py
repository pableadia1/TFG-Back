from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from Scraping.views import *

from Liga.models import Liga
from Equipo.models import Equipo
from Jugador.models import Jugador
from Estadisticas.models import *


# Create your tests here.

class LigaTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.liga1 = Liga.objects.create(nombre="La Liga",id=10,logo="La Liga.jpg",pais="Spain")

        self.equipo1 = Equipo.objects.create(nombre="equipo1",escudo="equipo1.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=28,liga=self.liga1,id=1)

        self.jugador1 = Jugador.objects.create(id=1,nombre="jugadorPrueba1",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="CC",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador2 = Jugador.objects.create(id=2,nombre="jugadorPrueba2",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador3 = Jugador.objects.create(id=3,nombre="jugadorPrueba3",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="DF",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador4 = Jugador.objects.create(id=4,nombre="jugadorPrueba4",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="DF",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador5 = Jugador.objects.create(id=5,nombre="jugadorPrueba5",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador6 = Jugador.objects.create(id=6,nombre="jugadorPrueba6",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="CC",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador7 = Jugador.objects.create(id=7,nombre="jugadorPrueba7",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="DL",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador8 = Jugador.objects.create(id=8,nombre="jugadorPrueba8",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="DL",foto="foto.jpg",equipoActual=self.equipo1)
        

        lisEstGen1 = [("2020-2021","Equipo1",30,27,2605,11,2)]
        lisEstGen2 = [("2020-2021","Equipo1",30,27,2605,9,3)]
        lisEstGen3 = [("2020-2021","Equipo1",30,27,2605,6,1)]
        lisEstGen4 = [("2020-2021","Equipo1",30,27,2605,1,10)]
        lisEstGen5 = [("2020-2021","Equipo1",30,27,2605,0,5)]
        lisEstGen6 = [("2020-2021","Equipo1",30,27,2605,3,4)]
        lisEstGen7 = [("2020-2021","Equipo1",30,27,2605,12,0)]
        lisEstGen8 = [("2020-2021","Equipo1",30,27,2605,14,0)]

        lisEstMisc1 = [(1,0,0,0,5,0,1,12,52,4)]

        lisEstTJ = [(22,6)]

        lisEstPor = [(43,127,72,8,5,0,2)]

        estGen1 = estadisticasGenerales(lisEstGen1,lisEstTJ,self.jugador1)
        estGen2 = estadisticasGenerales(lisEstGen2,lisEstTJ,self.jugador2)
        estGen3 = estadisticasGenerales(lisEstGen3,lisEstTJ,self.jugador3)
        estGen4 = estadisticasGenerales(lisEstGen4,lisEstTJ,self.jugador4)
        estGen5 = estadisticasGenerales(lisEstGen5,lisEstTJ,self.jugador5)
        estGen6 = estadisticasGenerales(lisEstGen6,lisEstTJ,self.jugador6)
        estGen7 = estadisticasGenerales(lisEstGen7,lisEstTJ,self.jugador7)
        estGen8 = estadisticasGenerales(lisEstGen8,lisEstTJ,self.jugador8)

        estadisticasMisc(lisEstMisc1,estGen1)
        estadisticasMisc(lisEstMisc1,estGen2)

        estadisticasPortero(lisEstPor,estGen2)

    def test_estadisticas_jugador(self):

        expected_result = [{
            "temporada": "2020-2021",
            "equipo": "Equipo1",
            "amarillas": 1,
            "rojas": 0,
            "goles_paradas": 11,
            "asistencias_cleanSheet": 2,
            "pj": 30,
            "titular": 27,
            "min": 2605
        }]

        response = self.client.get('/jugador/estadisticas/1')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_estadisticas_jugador_portero(self):

        expected_result = [{
            "temporada": "2020-2021",
            "equipo": "Equipo1",
            "amarillas": 1,
            "rojas": 0,
            "goles_paradas": 72,
            "asistencias_cleanSheet": 8,
            "pj": 30,
            "titular": 27,
            "min": 2605
        }]

        response = self.client.get('/jugador/estadisticas/2')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
            
    def tearDown(self):
        self.client = None
        self.liga1.delete()