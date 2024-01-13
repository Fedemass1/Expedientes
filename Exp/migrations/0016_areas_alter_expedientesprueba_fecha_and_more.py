# Generated by Django 5.0 on 2024-01-13 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exp', '0015_pases'),
    ]

    operations = [
        migrations.CreateModel(
            name='Areas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'areas',
            },
        ),
        migrations.AlterField(
            model_name='expedientesprueba',
            name='fecha',
            field=models.DateTimeField(default='13/01/2024'),
        ),
        migrations.AlterField(
            model_name='pases',
            name='fecha_pase',
            field=models.DateTimeField(default='13'),
        ),
    ]
