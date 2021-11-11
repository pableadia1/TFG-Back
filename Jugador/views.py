from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from Jugador.models import Jugador
from Equipo.models import Equipo
from .serializers import JugadorSerializer, JugadorSerializerEquipo

# Create your views here.

class jugadores(APIView):

    def get(self, request, id_equipo):
        jugadores = Jugador.objects.filter(equipoActual=id_equipo).order_by("fechaDeNacimiento")
        if len(jugadores) != 0:
                serializer = JugadorSerializerEquipo(jugadores, many="True")
                return Response(serializer.data)
        else :
            return Response({"mensaje":"No existe dicho equipo"},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id_equipo):
        try:
            posicion = request.data["pos"]
            jugadores = Jugador.objects.filter(equipoActual=id_equipo,posicion=posicion).order_by("fechaDeNacimiento")
        except:
            return Response({"mensaje":"Indique la posición"},status=status.HTTP_400_BAD_REQUEST)
        if len(jugadores) != 0:
                serializer = JugadorSerializerEquipo(jugadores, many="True")
                return Response(serializer.data)
        else :
            return Response({"mensaje":"No existe dicho equipo o posición"},status=status.HTTP_400_BAD_REQUEST)
          
class jugador(APIView):

    def get(self, request, id_jugador):
        try:
            jugador = Jugador.objects.get(id=id_jugador)
            serializer = JugadorSerializer(jugador)
            return Response(serializer.data)
        except:
            return Response({"mensaje":"No existe dicho jugador"},status=status.HTTP_400_BAD_REQUEST)