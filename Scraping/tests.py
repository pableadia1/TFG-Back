from unittest import result
from django.test import TestCase
from .views import *
from Jugador.models import Jugador

from bs4 import BeautifulSoup
import requests
import lxml

#equipo = Equipo.objects.create(nombre="equipo1",escudo="equipo1.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=28)


class SimpleTest(TestCase):

    def test_zeros(self):
        data = "70"
        resultado_esperado = 70  
        self.assertEqual(Zeros(data), resultado_esperado)
    
    def test_demarcaciones(self):
        data = "(MCO-DEL-EI)"
        resultado_esperado = ["MCO","DEL","EI"]
        self.assertEqual(demarcaciones(data), resultado_esperado)
   

    def test_yardMetrosDec(self):
        data = "24.7"
        resultado_esperado = "22.5"  
        self.assertEqual(yardMetrosDec(data), resultado_esperado)
    
    def test_yardMetros(self):
        data = "100"
        resultado_esperado = "91"  
        self.assertEqual(yardMetros(data), resultado_esperado)


class ScrappingTest(TestCase):
    def setUp(self):
        r = requests.get("https://fbref.com/es/jugadores/3f10bd22/Jesus-Navas").text
        r1 = requests.get("https://fbref.com/es/jugadores/f6798fc3/Yassine-Bounou").text
        self.s1 = BeautifulSoup(r, "lxml")
        self.s2 = BeautifulSoup(r1, "lxml")
    
    def test_creacion(self):
        res = creacion(self.s1)
        self.assertEqual(res[0],(9,0))
        self.assertEqual(len(res),4)
    
    def test_generales(self):
        res = generales(self.s1)
        self.assertEqual(res[0],("2018-2019","Sevilla",32, 31, 2712, 1, 5))
        self.assertEqual(len(res),4)
    
    def test_tiros(self):
        res = tiros(self.s1)
        self.assertEqual(res[0],(31,11,19.5,0,0,0))
        self.assertEqual(len(res),4)
    
    def test_pases(self):
        res = pases(self.s1)
        self.assertEqual(res[0],(23001,633,731,514,688,193,332))
        self.assertEqual(len(res),4)
    
    def test_tipopase(self):
        res = tipoPase(self.s1)
        self.assertEqual(res[0],(339,164,2,987,426,423,1374,145,82,33,12))
        self.assertEqual(len(res),4)
    
    def test_defensa(self):
        res = defensa(self.s1)
        self.assertEqual(res[0],(30,23,19,9,2,33,18,256,69,116,80,60))
        self.assertEqual(len(res),4)

    def test_posesion(self):
        res = posesion(self.s1)
        self.assertEqual(res[0],(2092, 93, 524, 885, 852, 87, 59, 40, 1444, 8869, 18, 1563, 1374))
        self.assertEqual(len(res),4)
    
    def test_misc(self):
        res = misc(self.s1)
        self.assertEqual(res[0],(8, 0, 0, 12, 31, 8, 0, 289, 11, 31))
        self.assertEqual(len(res),4)
    
    def test_portero(self):
        res = portero(self.s2)
        self.assertEqual(len(res),4)
        self.assertEqual(res[0],(43, 162, 126, 8, 6, 0, 0))
    
    def test_tempJuego(self):
        res = tempJuego(self.s1)
        self.assertEqual(res[0],(28, 1))
        self.assertEqual(len(res),4)
    

class LigaTest(TestCase):
    def setUp(self):
        res = requests.get("https://fbref.com/es/comps/12/Estadisticas-de-La-Liga").text
        r1 = res[:100000]
        s1 = BeautifulSoup(r1, "lxml").find("div", class_=["comps"])
        r = res[:180000]
        s = BeautifulSoup(r, "lxml").find("table", class_=["stats_table sortable min_width"])
        self.liga = obtenerLiga(s1,s)
        
    def test_liga(self):
        l = Liga.objects.get(id=self.liga[1].id)
        self.assertEqual((l.nombre,l.logo,l.pais),("La Liga","La Liga.jpg","Spain"))

    def tearDown(self):
        self.liga[1].delete()

class EquipoTest(TestCase):
    def setUp(self):
        self.liga = Liga.objects.create(nombre="l1",logo="l1.jpg",pais="Spain")
        res = requests.get("https://fbref.com/es/comps/12/Estadisticas-de-La-Liga").text
        r = res[:180000]
        s = BeautifulSoup(r, "lxml").find("table", class_=["stats_table sortable min_width"])
        tabla = s.find_all("tr")
        tabla = tabla[1:2]
        self.equipo = obtenerEquipos(tabla,self.liga)

    def test_equipo(self):
        eqp = Equipo.objects.get(id=self.equipo[1][0].id)
        self.assertEqual((eqp.nombre,eqp.escudo,eqp.partidosJugados,eqp.victorias,eqp.derrotas,eqp.empates,eqp.golesFavor,eqp.golesContra,eqp.puntos),("Real Sociedad","Real Sociedad.jpg",13,8,1,4,19,10,28))

    def tearDown(self):
        self.liga.delete()

class JugadorTest(TestCase):
    def setUp(self):
        self.liga = Liga.objects.create(nombre="l1",logo="l1.jpg",pais="Spain")
        self.equipo = Equipo.objects.create(nombre="equipo1",escudo="equipo1.jpg",partidosJugados=10,victorias=8,derrotas=2,empates=0,golesFavor=30,golesContra=8,puntos=28,liga=self.liga) 
        r = requests.get("https://fbref.com/es/equipos/e31d1cd9/Estadisticas-de-Real-Sociedad").text
        r = r[:190000]
        soup = BeautifulSoup(r,"lxml")
        s = soup.find("tbody").find("tr")
        self.jugador = datosJugador(s,self.equipo)
   
    def test_jugador(self):
        j = Jugador.objects.get(id=self.jugador[0].id)
        self.assertEqual((j.nombre,j.nombreCompleto,j.nacionalidad,j.fechaDeNacimiento,j.altura,j.peso,j.pie,j.posicion,j.demarcaciones,j.foto,j.equipoActual),("Robin Le Normand","Robin Le Normand","France",datetime.date(1996, 11, 11),187,84,"Derecha","DF",["DC"],"Robin Le Normand.jpg",self.equipo))

    def tearDown(self):
        self.liga.delete()

class ModeloTest(TestCase):
    def setUp(self):
        self.jugador = Jugador.objects.create(nombre="jugadorPrueba",nombreCompleto="jugadoPrueba",nacionalidad="España",pie="Izquierda",posicion="PO",foto="foto.jpg") 

        lisEstCr = [(5,7)]
        lisEstGen = [("2020-2021","EquipoPrueba",30,27,2605,12,6)]
        lisEstTJ = [(22,6)]
        lisEstDef = [(130,80,50,40,10,5,6,7,8,6,5,4)]
        lisEstMisc = [(3,45,3,5,3,2,0,1,0,59)]
        lisEstTiros = [(10,5,28.5,0,2,1)]
        lisEstPor = [(1,2,3,4,5,6,7)]
        lisEstPas = [(10,345,23,23,432,5,5)]
        lisEstTP =[(22,56,21,45,543,2,12,3,5,1,34)]
        lisEstPos = [(45,23,54,345,23,34,1,34,2,43,45,0,0)]

        self.gen = estadisticasGenerales(lisEstGen,lisEstTJ,self.jugador)
        self.cr = estadisticasCreacion(lisEstCr,self.gen)
        self.defn = estadisticasDefensa(lisEstDef,self.gen)
        self.misc = estadisticasMisc(lisEstMisc,self.gen)
        self.tir = estadisticasTiros(lisEstTiros,self.gen)
        self.por = estadisticasPortero(lisEstPor,self.gen)
        self.pas = estadisticasPases(lisEstPas,self.gen)
        self.tp = estadisticasTipoPase(lisEstTP,self.gen)
        self.pos = estadisticasPosesion(lisEstPos,self.gen)
    
    def test_generales(self):
        gen = EstadisticasGenerales.objects.get(id=self.gen[0].id)
        self.assertEqual((gen.partidosJugados,gen.titular,gen.partidosCompletos,gen.entraSuplente,gen.goles,gen.minutosJugados,gen.asistencias),(30,27,22,6,12,2605,6))

    def test_creacion(self):
        cr = EstadisticasCreacion.objects.get(id=self.cr[0].id)
        self.assertEqual((cr.pasesGol,cr.pasesMuertosGol),(5,7))
    
    def test_defensa(self):
        defn = EstadisticasDefensa.objects.get(id=self.defn[0].id)
        self.assertEqual((defn.entradas,defn.entradasGanadas),(130,80))
    
    def tearDown(self):
        self.jugador.delete()

