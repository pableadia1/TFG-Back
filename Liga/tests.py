from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from Scraping.views import estadisticasGenerales

from Liga.models import Liga
from Equipo.models import Equipo
from Jugador.models import Jugador
from Estadisticas.models import *

class LigaTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.liga1 = Liga.objects.create(nombre="La Liga",id=10,logo="La Liga.jpg",pais="Spain")
        self.liga2 = Liga.objects.create(nombre="La Liga 2",id=11,logo="La Liga 2.jpg",pais="Spain")

        self.equipo1 = Equipo.objects.create(nombre="equipo1",escudo="equipo1.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=28,liga=self.liga1,id=1)
        self.equipo2 = Equipo.objects.create(nombre="equipo2",escudo="equipo2.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=25,liga=self.liga1,id=2)
        self.equipo3 = Equipo.objects.create(nombre="equipo3",escudo="equipo3.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=24,liga=self.liga1,id=3)
        self.equipo4 = Equipo.objects.create(nombre="equipo4",escudo="equipo4.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=23,liga=self.liga1,id=4)
        self.equipo5 = Equipo.objects.create(nombre="equipo5",escudo="equipo5.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=20,liga=self.liga1,id=5)

        self.jugador1 = Jugador.objects.create(id=1,nombre="jugadorPrueba1",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador2 = Jugador.objects.create(id=2,nombre="jugadorPrueba2",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador3 = Jugador.objects.create(id=3,nombre="jugadorPrueba3",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador4 = Jugador.objects.create(id=4,nombre="jugadorPrueba4",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador5 = Jugador.objects.create(id=5,nombre="jugadorPrueba5",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador6 = Jugador.objects.create(id=6,nombre="jugadorPrueba6",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador7 = Jugador.objects.create(id=7,nombre="jugadorPrueba7",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador8 = Jugador.objects.create(id=8,nombre="jugadorPrueba8",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador9 = Jugador.objects.create(id=9,nombre="jugadorPrueba9",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador10 = Jugador.objects.create(id=10,nombre="jugadorPrueba10",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador11 = Jugador.objects.create(id=11,nombre="jugadorPrueba11",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador12 = Jugador.objects.create(id=12,nombre="jugadorPrueba12",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador13 = Jugador.objects.create(id=13,nombre="jugadorPrueba13",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador14 = Jugador.objects.create(id=14,nombre="jugadorPrueba14",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg",equipoActual=self.equipo1)

        lisEstGen1 = [("2020-2021","Equipo1",30,27,2605,11,2)]
        lisEstGen2 = [("2020-2021","Equipo1",30,27,2605,9,3)]
        lisEstGen3 = [("2020-2021","Equipo1",30,27,2605,6,1)]
        lisEstGen4 = [("2020-2021","Equipo1",30,27,2605,1,10)]
        lisEstGen5 = [("2020-2021","Equipo1",30,27,2605,0,5)]
        lisEstGen6 = [("2020-2021","Equipo1",30,27,2605,3,4)]
        lisEstGen7 = [("2020-2021","Equipo1",30,27,2605,12,0)]
        lisEstGen8 = [("2020-2021","Equipo1",30,27,2605,14,0)]
        lisEstGen9 = [("2020-2021","Equipo1",30,27,2605,6,1)]
        lisEstGen10 = [("2020-2021","Equipo1",30,27,2605,6,3)]
        lisEstGen11 = [("2020-2021","Equipo1",30,27,2605,5,0)]
        lisEstGen12 = [("2020-2021","Equipo1",30,27,2605,0,12)]
        lisEstGen13 = [("2020-2021","Equipo1",30,27,2605,0,6)]
        lisEstGen14 = [("2020-2021","Equipo1",30,27,2605,1,9)]

        lisEstTJ = [(22,6)]

        estadisticasGenerales(lisEstGen1,lisEstTJ,self.jugador1)
        estadisticasGenerales(lisEstGen2,lisEstTJ,self.jugador2)
        estadisticasGenerales(lisEstGen3,lisEstTJ,self.jugador3)
        estadisticasGenerales(lisEstGen4,lisEstTJ,self.jugador4)
        estadisticasGenerales(lisEstGen5,lisEstTJ,self.jugador5)
        estadisticasGenerales(lisEstGen6,lisEstTJ,self.jugador6)
        estadisticasGenerales(lisEstGen7,lisEstTJ,self.jugador7)
        estadisticasGenerales(lisEstGen8,lisEstTJ,self.jugador8)
        estadisticasGenerales(lisEstGen9,lisEstTJ,self.jugador9)
        estadisticasGenerales(lisEstGen10,lisEstTJ,self.jugador10)
        estadisticasGenerales(lisEstGen11,lisEstTJ,self.jugador11)
        estadisticasGenerales(lisEstGen12,lisEstTJ,self.jugador12)
        estadisticasGenerales(lisEstGen13,lisEstTJ,self.jugador13)
        estadisticasGenerales(lisEstGen14,lisEstTJ,self.jugador14)

    def test_liga_id(self):
        expected_result = [{
            "id": 10,
            "nombre": "La Liga",
            "logo":"La Liga.jpg",
            "pais": "Spain"
            }]

        response = self.client.get('/liga/10')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
        
    def test_ligas(self):
        expected_result = [{
            "id": 10,
            "nombre": "La Liga",
            "logo":"La Liga.jpg",
            "pais": "Spain"
            },
            {
            "id": 11,
            "nombre": "La Liga 2",
            "logo":"La Liga 2.jpg",
            "pais": "Spain"  
            }]

        response = self.client.get('/liga/0')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    
    def test_tabla(self):
        expected_result = [{
            "id":1,
            "nombre": "equipo1",
            "escudo": "equipo1.jpg",
            "partidosJugados":10,
            "victorias":8,
            "derrotas":2,
            "empates":0,
            "golesFavor":30,
            "golesContra":8,
            "puntos":28,
            "liga":10
        },
        {
            "id":2,
            "nombre": "equipo2",
            "escudo": "equipo2.jpg",
            "partidosJugados":10,
            "victorias":8,
            "derrotas":2,
            "empates":0,
            "golesFavor":30,
            "golesContra":8,
            "puntos":25,
            "liga":10
        },
        {
            "id":3,
            "nombre": "equipo3",
            "escudo": "equipo3.jpg",
            "partidosJugados":10,
            "victorias":8,
            "derrotas":2,
            "empates":0,
            "golesFavor":30,
            "golesContra":8,
            "puntos":24,
            "liga":10
        },
        {
            "id":4,
            "nombre": "equipo4",
            "escudo": "equipo4.jpg",
            "partidosJugados":10,
            "victorias":8,
            "derrotas":2,
            "empates":0,
            "golesFavor":30,
            "golesContra":8,
            "puntos":23,
            "liga":10
        },
        {
            "id":5,
            "nombre": "equipo5",
            "escudo": "equipo5.jpg",
            "partidosJugados":10,
            "victorias":8,
            "derrotas":2,
            "empates":0,
            "golesFavor":30,
            "golesContra":8,
            "puntos":20,
            "liga":10
        }]
        response = self.client.get('/liga/tabla/10')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_max_asistentes(self):

        data= {
            "temporada":"2020-2021",
            "dato":"asistencias"
        }

        expected_result = [{
            "id": 12,
            "nombre":"jugadorPrueba12",
            "estadistica":12,
            "equipo":"equipo1"
        },
        {
            "id": 4,
            "nombre":"jugadorPrueba4",
            "estadistica":10,
            "equipo":"equipo1"
        },
        {
            "id": 14,
            "nombre":"jugadorPrueba14",
            "estadistica":9,
            "equipo":"equipo1"
        }
        ]

        response = self.client.post('/liga/maximos/10', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values[:3], expected_result)
            
    def tearDown(self):
        self.client = None
        self.liga1.delete()
        self.liga2.delete()
