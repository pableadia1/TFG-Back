from rest_framework import serializers
from .models import Equipo

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = ["id","nombre","escudo","liga"]