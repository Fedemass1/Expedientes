from django.db import models


class Procucto(models.Model):
    titulo = models.TextField(max_length=200)
    descripcion = models.TextField(max_length=200)
    precio = models.IntegerField()


class Programmer(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=3)
    birthday = models.DateField()
    score = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'programmer'
