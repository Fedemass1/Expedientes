# Generated by Django 5.0 on 2024-01-18 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exp', '0004_alter_expedientesprueba_fecha'),
    ]

    operations = [
        migrations.CreateModel(
            name='Iniciadores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iniciador', models.CharField(max_length=100)),
                ('sigla', models.CharField(max_length=2)),
            ],
        ),
        migrations.AlterField(
            model_name='pases',
            name='fecha_pase',
            field=models.DateTimeField(default='18'),
        ),
    ]
