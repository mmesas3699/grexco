# Generated by Django 2.0.1 on 2018-06-25 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0011_tiposincidentes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tiposincidentes',
            old_name='codigo',
            new_name='id',
        ),
    ]
