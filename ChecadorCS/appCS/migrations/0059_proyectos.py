# Generated by Django 4.1.7 on 2023-03-24 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCS', '0058_alter_relacionnfcempleado_uid_nfc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proyectos',
            fields=[
                ('id_proyecto', models.AutoField(primary_key=True, serialize=False)),
                ('numero_proyecto_interno', models.CharField(max_length=255)),
                ('nombre_proyecto', models.CharField(max_length=255)),
                ('cliente', models.CharField(max_length=255)),
                ('lugar', models.CharField(max_length=255)),
            ],
        ),
    ]
