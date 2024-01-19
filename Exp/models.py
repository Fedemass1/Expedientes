from django.db import models
from datetime import datetime

from django.utils import timezone


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


class Areas(models.Model):
    area = models.CharField(max_length=100)

    class Meta:
        db_table = 'Areas'

    def __str__(self):
        return self.area


class Iniciadores(models.Model):
    iniciador = models.CharField(max_length=100)
    sigla = models.CharField(max_length=2)

    class Meta:
        db_table = 'Iniciadores'

    def __str__(self):
        return self.iniciador

    def save(self, *args, **kwargs):
        # Convierte la sigla a mayúsculas antes de guardarla
        self.sigla = self.sigla.upper()
        super(Iniciadores, self).save(*args, **kwargs)


# Uso este modelo para crear una BD de prueba y agregar nuevos expedientes.
class ExpedientesPrueba(models.Model):
    fecha = models.DateTimeField(default=timezone.now)  # Me muestra la fecha en el formato dd/mm/aaaa en la datatable. Esto se debe complementar con el JS
    nro_exp = models.IntegerField()
    iniciador = models.ForeignKey(Iniciadores, on_delete=models.CASCADE)
    objeto = models.TextField(max_length=500)
    nro_resol_rectorado = models.CharField(max_length=100, null=True, blank=True)
    nro_resol_CS = models.CharField(max_length=100, null=True, blank=True)
    observaciones = models.TextField(max_length=500, null=True, blank=True)
    area_creacion = models.ForeignKey(Areas,related_name='area_creacion', on_delete=models.CASCADE, null=True)
    exp_year = models.CharField(max_length=100, null=True, blank=True, unique=True)
    class Meta:
        db_table = 'expedientes_prueba'

    def __str__(self):
        return str(self.nro_exp)

    def save(self, *args, **kwargs):
        self.exp_year = f"{self.nro_exp}/{self.fecha.year}"
        super().save(*args, **kwargs)



class Pases(models.Model):
    nro_exp = models.ForeignKey(ExpedientesPrueba, related_name='pases', on_delete=models.CASCADE, null=True, blank=True)
    fecha_pase = models.DateTimeField(default=datetime.now().date().strftime("%d"))
    area_origen = models.ForeignKey(Areas, related_name='area_origen', on_delete=models.CASCADE, null=True)
    area_receptora = models.ForeignKey(Areas, related_name='area_receptora', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'expedientes_pases'






