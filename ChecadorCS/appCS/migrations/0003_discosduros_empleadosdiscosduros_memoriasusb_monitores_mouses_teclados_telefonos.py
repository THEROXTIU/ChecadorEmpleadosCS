# Generated by Django 3.2.5 on 2022-01-20 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appCS', '0002_alter_respuestas_respuesta'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscosDuros',
            fields=[
                ('id_disco', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=30)),
                ('marca', models.CharField(max_length=30)),
                ('capacidad', models.IntegerField(null=True)),
                ('dimension', models.CharField(max_length=20)),
                ('alm_uso', models.IntegerField(null=True)),
                ('alm_libre', models.IntegerField(null=True)),
                ('estado', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='MemoriasUSB',
            fields=[
                ('id_usb', models.AutoField(primary_key=True, serialize=False)),
                ('marca', models.CharField(max_length=30)),
                ('modelo', models.CharField(max_length=30)),
                ('capacidad', models.IntegerField()),
                ('cantidadStock', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Telefonos',
            fields=[
                ('id_telefono', models.AutoField(primary_key=True, serialize=False)),
                ('conexion', models.CharField(max_length=2)),
                ('marca', models.CharField(max_length=30)),
                ('modelo', models.CharField(max_length=30)),
                ('estado', models.CharField(max_length=30)),
                ('foto', models.ImageField(null=True, upload_to='telefonos')),
                ('extension', models.CharField(max_length=10, null=True)),
                ('nodo', models.CharField(max_length=20, null=True)),
                ('activo', models.CharField(max_length=2)),
                ('id_empleado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appCS.empleados')),
            ],
        ),
        migrations.CreateModel(
            name='Teclados',
            fields=[
                ('id_teclado', models.AutoField(primary_key=True, serialize=False)),
                ('conexion', models.CharField(max_length=2)),
                ('marca', models.CharField(max_length=30)),
                ('modelo', models.CharField(max_length=30)),
                ('estado', models.CharField(max_length=30)),
                ('foto', models.ImageField(null=True, upload_to='teclados')),
                ('activo', models.CharField(max_length=2)),
                ('id_equipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appCS.equipos')),
            ],
        ),
        migrations.CreateModel(
            name='Mouses',
            fields=[
                ('id_mouse', models.AutoField(primary_key=True, serialize=False)),
                ('conexion', models.CharField(max_length=2)),
                ('marca', models.CharField(max_length=30)),
                ('modelo', models.CharField(max_length=30)),
                ('estado', models.CharField(max_length=30)),
                ('foto', models.ImageField(null=True, upload_to='mouses')),
                ('activo', models.CharField(max_length=2)),
                ('id_equipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appCS.equipos')),
            ],
        ),
        migrations.CreateModel(
            name='Monitores',
            fields=[
                ('id_monitor', models.AutoField(primary_key=True, serialize=False)),
                ('marca', models.CharField(max_length=30)),
                ('modelo', models.CharField(max_length=30)),
                ('estado', models.CharField(max_length=30)),
                ('foto', models.ImageField(null=True, upload_to='monitores')),
                ('activo', models.CharField(max_length=2)),
                ('id_equipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appCS.equipos')),
            ],
        ),
        migrations.CreateModel(
            name='EmpleadosDiscosDuros',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_disco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCS.discosduros')),
                ('id_empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCS.empleados')),
            ],
        ),
    ]
