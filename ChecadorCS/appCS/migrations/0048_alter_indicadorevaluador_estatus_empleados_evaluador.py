# Generated by Django 4.0.4 on 2023-01-03 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCS', '0047_alter_indicadorevaluador_empleados_evaluados_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicadorevaluador',
            name='estatus_empleados_evaluador',
            field=models.CharField(max_length=255),
        ),
    ]
