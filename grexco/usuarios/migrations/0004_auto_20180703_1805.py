# Generated by Django 2.0.1 on 2018-07-03 18:05

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_auto_20180703_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adjuntos',
            name='archivo',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/mnt/c/User/arju/Desktop/Grexco/Proyectos/Web/grexco/usuarios/'), upload_to='incidentes/<django.db.models.fields.related.ForeignKey>/'),
        ),
    ]
