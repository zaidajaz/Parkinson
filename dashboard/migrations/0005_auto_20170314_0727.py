# Generated by Django 2.0.dev20170221005733 on 2017-03-14 07:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20170314_0727'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlgoList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algo_name', models.CharField(max_length=200)),
                ('algo_display_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='datainfo',
            name='dataset_up_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 3, 14, 7, 27, 57, 490819)),
        ),
        migrations.AlterField(
            model_name='modelinfo',
            name='model_up_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 3, 14, 7, 27, 57, 498874)),
        ),
    ]
