from django.db import models
from Liga.models import Liga

class Equipo(models.Model):
    nombre = models.CharField(max_length= 80)
    escudo = models.CharField(max_length= 200)
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE)
    partidosJugados = models.IntegerField()
    victorias = models.IntegerField()
    derrotas = models.IntegerField()
    empates = models.IntegerField()
    golesFavor = models.IntegerField()
    golesContra = models.IntegerField()
    puntos  = models.IntegerField()
    objects = models.Manager()
