# Generated by Django 4.0.4 on 2022-10-31 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appCS', '0036_tenenciasvehiculos_ano_pagado_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='reparacionVehiculo',
            fields=[
                ('id_reparacion', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_reparacion', models.DateField()),
                ('motivo_reparacion', models.CharField(max_length=25)),
                ('descripcion_reparacion', models.CharField(max_length=255)),
                ('taller_reparacion', models.CharField(max_length=100, null=True)),
                ('costo_reparacion', models.FloatField()),
                ('factura_reparacion', models.FileField(null=True, upload_to='facturaReparacion')),
                ('agregado_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCS.empleados')),
                ('id_vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCS.vehiculos')),
            ],
        ),
    ]
