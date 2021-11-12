from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status

from Estadisticas.models import *
from .serializers import *

class estadisticasJugador(APIView):
    def get(self,request, id_jugador):
        jug = EstadisticasJugador.objects.filter(jugador=id_jugador)
        if len(jug) == 0:
            res = []
        else:
            estadisticas = []
            for j in jug:
                gen = EstadisticasGenerales.objects.get(id = j.estadisticasGenerales.id)
                if j.estadisticasDiversas == None:
                    amarillas,rojas = 0,0
                else:
                    misc = EstadisticasDiversas.objects.get(id = j.estadisticasDiversas.id)
                    amarillas,rojas = misc.amarillas,misc.rojas
                if j.jugador.posicion != "PO":
                    est = Estadisticas(temporada=j.temporada, equipo= j.equipo, amarillas= amarillas, rojas= rojas, asistencias_cleanSheet= gen.asistencias, pj= gen.partidosJugados,
                    titular= gen.titular, min = gen.minutosJugados, goles_paradas= gen.goles)
                else:
                    if j.estadisticasPortero == None:
                        paradas, cleanSheet = 0,0
                    else:
                        por = EstadisticasPortero.objects.get(id = j.estadisticasPortero.id)
                        paradas, cleanSheet = por.paradasRecibidos,por.cleanSheet
                    est = Estadisticas(temporada=j.temporada, equipo= j.equipo, amarillas= misc.amarillas, rojas= misc.rojas, asistencias_cleanSheet=cleanSheet, pj= gen.partidosJugados,
                    titular= gen.titular, min = gen.minutosJugados, goles_paradas = paradas)
                estadisticas.append(est)
                estadisticas.sort(key = lambda x:x.temporada)    
            serializer = EstadisticasJug(estadisticas, many="True")
            res = serializer.data
        return Response(res)
