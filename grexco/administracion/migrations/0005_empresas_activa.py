# Generated by Django 2.0.1 on 2018-06-05 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0004_auto_20180531_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresas',
            name='activa',
            field=models.BooleanField(default=True),
        ),
    ]
