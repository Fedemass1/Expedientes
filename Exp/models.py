from django.db import models
from datetime import datetime


class Expedientes(models.Model):
    fecha = models.DateField()
    nro_exp = models.CharField(max_length=100)
    iniciador = models.CharField(max_length=100, null=True, blank=True)
    objeto = models.TextField(max_length=200, null=True, blank=True)
    nro_resol_rectorado = models.CharField(max_length=100, null=True, blank=True)
    nro_resol_CS = models.CharField(max_length=100, null=True, blank=True)
    observaciones = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'expedientes'


# Uso este modelo para crear una BD de prueba y agregar nuevos expedientes.
class ExpedientesPrueba(models.Model):
    fecha = models.DateTimeField(default=datetime.now().date().strftime(
        "%d/%m/%Y"))  # Me muestra la fecha en el formato dd/mm/aaaa en la datatable. Esto se debe complementar con el JS
    nro_exp = models.IntegerField()
    iniciador = models.CharField(max_length=100)
    objeto = models.TextField(max_length=200)
    nro_resol_rectorado = models.CharField(max_length=100, null=True, blank=True)
    nro_resol_CS = models.CharField(max_length=100, null=True, blank=True)
    observaciones = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'expedientes_prueba'


class Pases(models.Model):
    nro_exp = models.ForeignKey(Expedientes, related_name='expedientes', on_delete=models.CASCADE, null=True)
    fecha_pase = models.DateTimeField(default=datetime.now().date().strftime("%d"))
    area = models.CharField(max_length=100)

    class Meta:
        db_table = 'expedientes_pases'
