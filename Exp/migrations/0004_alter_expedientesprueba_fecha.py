# Generated by Django 5.0 on 2024-01-17 21:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exp', '0003_alter_expedientesprueba_fecha_alter_pases_fecha_pase_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expedientesprueba',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
