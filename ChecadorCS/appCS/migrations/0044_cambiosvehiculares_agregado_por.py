# Generated by Django 4.0.4 on 2022-12-13 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appCS', '0043_remove_asignacionesvehiculares_encargado_asignado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cambiosvehiculares',
            name='agregado_por',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appCS.empleados'),
        ),
    ]
