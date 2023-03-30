# Generated by Django 4.0.4 on 2023-02-22 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appCS', '0053_faltasasistencia'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsistenciaProyectoForaneo',
            fields=[
                ('id_asistencia_proyecto_foraneo', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(null=True)),
                ('hora_entrada', models.CharField(max_length=8, null=True)),
                ('hora_salida', models.CharField(max_length=8, null=True)),
                ('proyecto_interno', models.CharField(max_length=100)),
                ('id_empleado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appCS.empleados')),
            ],
        ),
    ]
