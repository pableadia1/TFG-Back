from django.db import models

class Liga(models.Model):
    nombre = models.CharField(max_length= 80)
    logo = models.CharField(max_length= 200)
    pais = models.CharField(max_length= 100)
    objects = models.Manager()
