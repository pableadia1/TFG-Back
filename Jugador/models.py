from django.db import models
from Equipo.models import Equipo
from django.contrib.postgres.fields import ArrayField

class Jugador(models.Model):
    nombre = models.CharField(max_length= 50)
    nombreCompleto = models.CharField(max_length= 80)
    nacionalidad = models.CharField(max_length= 40)
    fechaDeNacimiento = models.DateField( null=True)
    altura = models.FloatField( null=True)
    peso = models.FloatField( null=True)
    pie = models.CharField(max_length=10, choices=(("Izquierda","Zurdo"),("Derecha","Diestro"),("Ambos","Ambidiestro")))
    posicion =   models.CharField(max_length= 2, choices=(("PO","Portero"),("DF", "Defensa"), ("CC", "CentroCampista"), ("DL", "Delantero")))
    demarcaciones = ArrayField(models.CharField(max_length= 3), null=True)
    equipoActual = models.ForeignKey(Equipo,on_delete=models.CASCADE, null=True)
    foto = models.CharField(max_length= 150)
    objects = models.Manager()
