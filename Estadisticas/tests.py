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
        self.jugador3 = Jugador.objects.create(id=3,nombre="jugadorPrueba3",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="DF",demarcaciones=[],foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador4 = Jugador.objects.create(id=4,nombre="jugadorPrueba4",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="DL",foto="foto.jpg",equipoActual=self.equipo1)

        lisEstGen1 = [("2020-2021","Equipo1",30,27,2605,11,2)]
        lisEstGen2 = [("2020-2021","Equipo1",5,2,283,1,3)]
        lisEstGen3 = [("2020-2021","Equipo1",103,99,8345,3,2)]
        lisEstGen4 = [("2020-2021","Equipo1",60,27,4302,30,22)]

        lisEstMisc1 = [(3,1,0,23,145,6,1,12,52,45)]
        lisEstMisc2 = [(1,0,0,0,5,0,1,12,52,12)]
        lisEstMisc3 = [(1,0,0,0,5,0,1,12,52,4)]
        lisEstMisc4 = [(1,0,0,0,5,0,1,12,52,4)]

        lisEstTJ = [(22,6)]

        lisEstPor1 = [(43,127,72,8,5,0,2)]
        lisEstPor2 = [(43,127,72,8,5,0,2)]

        lisEstCr = [(5,7)]

        lisEstDef1 = [(130,80,50,40,10,5,6,7,8,6,5,4)]
        lisEstDef2 = [(130,80,50,40,10,5,6,7,8,6,5,4)]

        lisEstTiros1 = [(10,5,28.5,0,2,1)]
        lisEstTiros2 = [(10,5,28.5,0,2,1)]

        lisEstPas1 = [(10,345,23,23,432,5,5)]
        lisEstPas2 = [(10,345,23,23,432,5,5)]

        lisEstTP1 =[(22,56,21,45,543,2,12,3,5,1,34)]
        lisEstTP2 =[(22,56,21,45,543,2,12,3,5,1,34)]

        lisEstPos1 = [(45,23,54,345,23,34,1,34,2,43,45,0,0)]
        lisEstPos2 = [(45,23,54,345,23,34,1,34,2,43,45,0,0)]

        estGen1 = estadisticasGenerales(lisEstGen1,lisEstTJ,self.jugador1)
        estGen2 = estadisticasGenerales(lisEstGen2,lisEstTJ,self.jugador2)
        estGen3 = estadisticasGenerales(lisEstGen3,lisEstTJ,self.jugador3)
        estGen4 = estadisticasGenerales(lisEstGen4,lisEstTJ,self.jugador4)


        estadisticasMisc(lisEstMisc1,estGen1)
        estadisticasMisc(lisEstMisc2,estGen2)
        estadisticasMisc(lisEstMisc1,estGen3)
        estadisticasMisc(lisEstMisc2,estGen4)

        estadisticasPortero(lisEstPor1,estGen2)
        estadisticasPortero(lisEstPor1,estGen3)
        estadisticasCreacion(lisEstCr,estGen3)
        estadisticasDefensa(lisEstDef1,estGen3)
        estadisticasPases(lisEstPas1,estGen3)
        estadisticasTipoPase(lisEstTP1,estGen3)
        estadisticasTiros(lisEstTiros1,estGen3)

    def test_estadisticas_jugador(self):

        expected_result = [{
            "temporada": "2020-2021",
            "equipo": "Equipo1",
            "posicion" : "CC",
            "amarillas": 3,
            "rojas": 1,
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
            "posicion" : "PO",
            "amarillas": 1,
            "rojas": 0,
            "goles_paradas": 72,
            "asistencias_cleanSheet": 8,
            "pj": 5,
            "titular": 2,
            "min": 283
        }]

        response = self.client.get('/jugador/estadisticas/2')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_notas_jugador(self):

        expected_result = [{
            "efectividad": 5.0,
            "tiros": 5.0,
            "pasesCortos": 5.0,
            "pasesLargos": 5.0,
            "entradas": 5.0,
            "presion": 5.0,
            "paraRegates": 5.0,
            "regates": 0.0,
            "controles": 3.0,
            "balonesAereos": 3.0,
            "temperamento": 10.0,
            "recuperaciones": 3,
            "paradas": 5.7,
            "sinGoles": 10.0
        }]

        response = self.client.get('/jugador/notas/3')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_notas_jugador_mal(self):

        expected_result = {
            "mensaje" : "No existe dicho jugador"
        }

        response = self.client.get('/jugador/notas/45')
        self.assertEqual(response.status_code, 400)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_caracteristicas_jugador(self):

        expected_result = [{
            "caracteristicas" : ['Recibe muchas faltas']
        }]

        response = self.client.get('/jugador/caracteristicas/1')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_caracteristicas_jugador_mal(self):

        expected_result = {
            "mensaje" : "No existe dicho jugador"
        }

        response = self.client.get('/jugador/caracteristicas/45')
        self.assertEqual(response.status_code, 400)

        values = response.json()
        self.assertEqual(values, expected_result)
            
    def tearDown(self):
        self.client = None
        self.liga1.delete()