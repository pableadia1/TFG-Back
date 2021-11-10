from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from Liga.models import Liga
from Equipo.models import Equipo
from .serializers import EquipoSerializer


class equipos(APIView):

    def get(self, request, id_liga):
        equipos = Equipo.objects.filter(liga_id=id_liga).order_by("-puntos")
        if len(equipos) != 0:
            serializer = EquipoSerializer(equipos, many="True")
            return Response(serializer.data)
        else :
            return Response({"mensaje":"No existe dicha liga"},status=status.HTTP_400_BAD_REQUEST)
    
class equipo(APIView):

    def get(self, request, id_equipo):
        try:
            equipo = Equipo.objects.get(id=id_equipo)
            serializer = EquipoSerializer(equipo)
            return Response(serializer.data)
        except:
            return Response({"mensaje":"No existe dicho equipo"},status=status.HTTP_400_BAD_REQUEST)





