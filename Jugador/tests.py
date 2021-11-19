from django.http.response import JsonResponse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from Liga.models import Liga
from Equipo.models import Equipo
from .models import Jugador
from Estadisticas.models import *

from datetime import date


# Create your tests here.

class JugadorTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.liga1 = Liga.objects.create(nombre="La Liga",id=10,logo="La Liga.jpg",pais="Spain")

        self.equipo1 = Equipo.objects.create(nombre="equipo1",escudo="equipo1.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=28,liga=self.liga1,id=1)

        self.jugador1 = Jugador.objects.create(id=1,nombre="jugadorPrueba1",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",fechaDeNacimiento=date(1981,12,1),foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador2 = Jugador.objects.create(id=2,nombre="jugadorPrueba2",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="DF",fechaDeNacimiento=date(1999,12,1),foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador3 = Jugador.objects.create(id=3,nombre="jugadorPrueba3",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="CC",fechaDeNacimiento=date(1998,12,1),foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador4 = Jugador.objects.create(id=4,nombre="jugadorPrueba4",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="DL",fechaDeNacimiento=date(1997,12,1),foto="foto.jpg",equipoActual=self.equipo1)
        self.jugador5 = Jugador.objects.create(id=5,nombre="jugadorPrueba5",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",fechaDeNacimiento=date(1996,12,1),foto="foto.jpg",equipoActual=self.equipo1)
 
    def test_jugadores_equipo(self):

        expected_result =  [{
            "nombre":"jugadorPrueba1",
            "fechaDeNacimiento": "1981-12-01",
            "foto": "foto.jpg",
            "nacionalidad":"España",
            "id":1
        },
        {
            "nombre":"jugadorPrueba5",
            "fechaDeNacimiento": "1996-12-01",
            "foto": "foto.jpg",
            "nacionalidad":"España",
            "id":5
        },
        {
            "nombre":"jugadorPrueba4",
            "fechaDeNacimiento": "1997-12-01",
            "foto": "foto.jpg",
            "nacionalidad":"España",
            "id":4
        },
        {
            "nombre":"jugadorPrueba3",
            "fechaDeNacimiento": "1998-12-01",
            "foto": "foto.jpg",
            "nacionalidad":"España",
            "id":3
        },
        {
            "nombre":"jugadorPrueba2",
            "fechaDeNacimiento": "1999-12-01",
            "foto": "foto.jpg",
            "nacionalidad":"España",
            "id":2
        }]  
        response = self.client.get('/jugador/todos/1')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_jugadores_equipo_posicion(self):

        expected_result =  [
        {
            "nombre":"jugadorPrueba4",
            "fechaDeNacimiento": "1997-12-01",
            "foto": "foto.jpg",
            "nacionalidad":"España",
            "id":4
        }]
        response = self.client.post('/jugador/todos/1',{"pos":"DL"},format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_jugador(self):

        expected_result = {
            'altura': None,
            'demarcaciones': None,
            'peso': None,
            "nombre":"jugadorPrueba3",
            "nombreCompleto":"jugadoPrueba",
            "fechaDeNacimiento": "1998-12-01",
            "foto": "foto.jpg",
            "nacionalidad":"España",
            "pie":"Izquierda",
            "posicion":"CC",
            "equipoActual":1,
            "id":3
        }
        response = self.client.get('/jugador/3')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
            
    def tearDown(self):
        self.client = None
        self.liga1.delete()
