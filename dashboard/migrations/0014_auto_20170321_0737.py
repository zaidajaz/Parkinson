# Generated by Django 2.0.dev20170221005733 on 2017-03-21 07:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_auto_20170320_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportinfo',
            name='report_accuracy',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='datainfo',
            name='dataset_up_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 3, 21, 7, 37, 16, 111950)),
        ),
        migrations.AlterField(
            model_name='modelinfo',
            name='model_up_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 3, 21, 7, 37, 16, 112603)),
        ),
        migrations.AlterField(
            model_name='reportinfo',
            name='report_up_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 3, 21, 7, 37, 16, 113514)),
        ),
    ]
