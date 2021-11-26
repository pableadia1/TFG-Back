from rest_framework import serializers
from Estadisticas.models import *

class Estadisticas:
    def __init__(self,temporada,equipo,posicion,amarillas,rojas,goles_paradas,asistencias_cleanSheet,pj,titular,min):
        self.temporada = temporada
        self.posicion = posicion
        self.equipo = equipo
        self.amarillas = amarillas
        self.rojas = rojas
        self.goles_paradas = goles_paradas
        self.asistencias_cleanSheet= asistencias_cleanSheet
        self.pj = pj
        self.titular = titular
        self.min = min
        
class EstadisticasJug(serializers.Serializer):
    temporada = serializers.CharField()
    equipo = serializers.CharField()
    posicion = serializers.CharField()
    amarillas = serializers.IntegerField()
    rojas = serializers.IntegerField()
    goles_paradas = serializers.IntegerField()
    asistencias_cleanSheet = serializers.IntegerField()
    pj = serializers.IntegerField()
    titular = serializers.IntegerField()
    min = serializers.IntegerField()

class Notas:
    def __init__(self,efectividad,tiros,pasesCortos,pasesLargos,entradas,presion,paraRegates,regates,controles,balonesAereos,temperamento,recuperaciones,paradas,sinGoles):
        self.efectividad = efectividad
        self.tiros = tiros
        self.pasesCortos = pasesCortos
        self.pasesLargos = pasesLargos
        self.entradas = entradas
        self.presion = presion
        self.paraRegates = paraRegates
        self.regates = regates
        self.controles = controles
        self.balonesAereos = balonesAereos
        self.temperamento = temperamento
        self.recuperaciones = recuperaciones
        self.paradas = paradas
        self.sinGoles = sinGoles

class NotasSerializar(serializers.Serializer):
    efectividad = serializers.FloatField()
    tiros = serializers.FloatField()
    pasesCortos = serializers.FloatField()
    pasesLargos = serializers.FloatField()
    entradas = serializers.FloatField()
    presion = serializers.FloatField()
    paraRegates = serializers.FloatField()
    regates = serializers.FloatField()
    controles = serializers.FloatField()
    balonesAereos = serializers.FloatField()
    temperamento = serializers.FloatField()
    recuperaciones = serializers.FloatField()
    paradas = serializers.FloatField()
    sinGoles = serializers.FloatField()

class Caracteristicas:
    def __init__(self,caracteristicas):
        self.caracteristicas = caracteristicas

class CaracteristicasSerializar(serializers.Serializer):
    caracteristicas = serializers.ListField()