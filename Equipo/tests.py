from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from Liga.models import Liga
from Equipo.models import Equipo

from Estadisticas.models import *

class LigaTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.liga1 = Liga.objects.create(nombre="La Liga",id=10,logo="La Liga.jpg",pais="Spain")
        self.liga2 = Liga.objects.create(nombre="La Liga 2",id=11,logo="La Liga 2.jpg",pais="Italy")

        self.equipo1 = Equipo.objects.create(nombre="equipo1",escudo="equipo1.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=28,liga=self.liga1,id=1)
        self.equipo2 = Equipo.objects.create(nombre="equipo2",escudo="equipo2.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=25,liga=self.liga1,id=2)
        self.equipo3 = Equipo.objects.create(nombre="equipo3",escudo="equipo3.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=24,liga=self.liga1,id=3)
        self.equipo4 = Equipo.objects.create(nombre="equipo4",escudo="equipo4.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=23,liga=self.liga1,id=4)
        self.equipo5 = Equipo.objects.create(nombre="equipo5",escudo="equipo5.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=20,liga=self.liga1,id=5)

        self.equipo1 = Equipo.objects.create(nombre="equipo6",escudo="equipo6.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=28,liga=self.liga2,id=6)
        self.equipo2 = Equipo.objects.create(nombre="equipo7",escudo="equipo7.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=25,liga=self.liga2,id=7)
        self.equipo3 = Equipo.objects.create(nombre="equipo8",escudo="equipo8.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=24,liga=self.liga2,id=8)
        self.equipo4 = Equipo.objects.create(nombre="equipo9",escudo="equipo9.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=23,liga=self.liga2,id=9)
        self.equipo5 = Equipo.objects.create(nombre="equipo10",escudo="equipo10.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=20,liga=self.liga2,id=10)

    def test_equipos_liga(self):

        expected_result = [{
            "id":1,
            "nombre": "equipo1",
            "escudo": "equipo1.jpg",
            "liga":10
        },
        {
            "id":2,
            "nombre": "equipo2",
            "escudo": "equipo2.jpg",
            "liga":10
        },
        {
            "id":3,
            "nombre": "equipo3",
            "escudo": "equipo3.jpg",
            "liga":10
        },
        {
            "id":4,
            "nombre": "equipo4",
            "escudo": "equipo4.jpg",
            "liga":10
        },
        {
            "id":5,
            "nombre": "equipo5",
            "escudo": "equipo5.jpg",
            "liga":10
        }]
        response = self.client.get('/equipo/todos/10')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_equipo(self):
        
        expected_result=[{
            "id":8,
            "nombre": "equipo8",
            "escudo": "equipo8.jpg",
            "liga":11
        }]

        response = self.client.get('/equipo/8')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def tearDown(self):
            self.client = None
            self.liga1.delete()
            self.liga2.delete()