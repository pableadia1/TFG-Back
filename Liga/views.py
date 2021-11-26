from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from Liga.models import Liga
from Equipo.models import Equipo
from Jugador.models import Jugador
from Estadisticas.models import EstadisticasJugador

from .serializers import LigaSerializer, EquipoSerializer, Maximos, MaximosSerializer

class ligas(APIView):

    def get(self, request, id_liga):
        if id_liga == 0:
            ligas = Liga.objects.all()
            serializer = LigaSerializer(ligas, many="True")
            return Response(serializer.data)
        else:
            try:
                liga = Liga.objects.get(id=id_liga)
                serializer = LigaSerializer([liga],many="True")
                return Response(serializer.data)           
            except:   
                return Response({"mensaje":"No existe dicha liga"},status=status.HTTP_400_BAD_REQUEST)

class tabla(APIView):
    
    def get(self, request, id_liga):
        equipos = Equipo.objects.filter(liga_id=id_liga).order_by("-puntos")
        serializer = EquipoSerializer(equipos, many="True")
        if len(equipos) == 0:
            return Response({"mensaje":"No existe dicha liga"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data)

class maximosEstadisticas(APIView):

    def tipoEstadistica(self,dato,est):
        if dato == "goles":
            res = est.estadisticasGenerales.goles
        elif dato == "asistencias":
            res = est.estadisticasGenerales.asistencias
        elif dato == "minutosJugados":
            res = est.estadisticasGenerales.minutosJugados
        elif dato == "amarillas":
            res = est.estadisticasDiversas.amarillas
        elif dato == "rojas":
            res = est.estadisticasDiversas.rojas
        elif dato == "faltasRecibidas":
            res = est.estadisticasDiversas.faltasRecibidas
        elif dato == "faltasCometidas":
            res = est.estadisticasDiversas.faltasCometidas
        else:
            res = "fallo"
        return res

    def post(self,request,id_liga):
        try:
            temporada = request.data["temporada"]
            dato = request.data["dato"]
            res = []
            if dato == "goles" or dato == "asistencias" or dato =="minutosJugados":
                estadisticas = EstadisticasJugador.objects.filter(temporada=temporada).order_by("-estadisticasGenerales__" + dato)
            elif dato=="amarillas" or dato == "rojas" or dato=="faltasRecibidas" or dato=="faltasCometidas":
                estadisticas = EstadisticasJugador.objects.filter(temporada=temporada,estadisticasDiversas_id__isnull=False).order_by("-estadisticasDiversas__" + dato)
                print(estadisticas[0].jugador.nombre)
            else:
                estadisticas= [1,2,3,4,5,6,7,8,9,10]

            for e in estadisticas[:10]:
                estadistica = self.tipoEstadistica(dato,e)
                if estadistica == "fallo":
                    return Response({"mensaje":"especifique bien el dato"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    jug = Jugador.objects.get(id=e.jugador.id)
                    nombre, equipo, id, id_jugador = jug.nombre, jug.equipoActual.nombre, jug.equipoActual.liga_id, jug.id
                    g = Maximos(nombre=nombre,estadistica=estadistica,equipo=equipo,id=id_jugador)
                    if id_liga != 0:
                        if id == id_liga:
                            res.append(g)
                    else:
                        res.append(g)
            if len(res) == 0:
                return Response({"mensaje":"no existe dicha liga o temporada"},status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = MaximosSerializer(res,many="True")
                return Response(serializer.data)
        except:
            return Response({"mensaje":"los parametros temporada y dato deben aparecer en el body"},status=status.HTTP_400_BAD_REQUEST)
 