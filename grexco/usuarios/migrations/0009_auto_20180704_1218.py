# Generated by Django 2.0.1 on 2018-07-04 12:18

import django.core.files.storage
from django.db import migrations, models
import usuarios.models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0008_auto_20180704_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adjuntos',
            name='archivo',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/mnt/c/User/arju/Desktop/Grexco/Proyectos/Web/grexco/usuarios/'), upload_to=usuarios.models.my_awesome_upload_function),
        ),
    ]
