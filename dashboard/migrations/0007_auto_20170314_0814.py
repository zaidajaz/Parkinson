# Generated by Django 2.0.dev20170221005733 on 2017-03-14 08:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20170314_0749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datainfo',
            name='dataset_up_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 3, 14, 8, 14, 50, 649886)),
        ),
        migrations.AlterField(
            model_name='modelinfo',
            name='model_algo',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='modelinfo',
            name='model_up_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 3, 14, 8, 14, 50, 650640)),
        ),
    ]