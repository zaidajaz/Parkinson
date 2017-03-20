# Generated by Django 2.0.dev20170221005733 on 2017-03-20 11:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_auto_20170316_0853'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_name', models.CharField(max_length=200)),
                ('report_author', models.CharField(max_length=200)),
                ('report_up_date', models.DateTimeField(blank=True, default=datetime.datetime(2017, 3, 20, 11, 4, 0, 474909))),
                ('report_model_id', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='datainfo',
            name='dataset_up_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 3, 20, 11, 4, 0, 473367)),
        ),
        migrations.AlterField(
            model_name='modelinfo',
            name='model_up_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 3, 20, 11, 4, 0, 473989)),
        ),
    ]
