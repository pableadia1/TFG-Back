from rest_framework import serializers
from Estadisticas.models import *

class Estadisticas:
    def __init__(self,temporada,equipo,amarillas,rojas,goles_paradas,asistencias_cleanSheet,pj,titular,min):
        self.temporada = temporada
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
    amarillas = serializers.IntegerField()
    rojas = serializers.IntegerField()
    goles_paradas = serializers.IntegerField()
    asistencias_cleanSheet = serializers.IntegerField()
    pj = serializers.IntegerField()
    titular = serializers.IntegerField()
    min = serializers.IntegerField()