from django.db.models import fields
from rest_framework import serializers
from Liga.models import Liga
from Equipo.models import Equipo

class LigaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liga
        fields = '__all__'

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model= Equipo
        fields = '__all__'

class Maximos:
    def __init__(self,nombre,estadistica,equipo):
        self.nombre = nombre
        self.estadistica = estadistica
        self.equipo = equipo

class MaximosSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    estadistica = serializers.IntegerField()
    equipo = serializers.CharField()