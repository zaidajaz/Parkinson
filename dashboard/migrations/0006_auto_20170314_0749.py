# Generated by Django 2.0.dev20170221005733 on 2017-03-14 07:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20170314_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datainfo',
            name='dataset_up_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 3, 14, 7, 49, 47, 449671)),
        ),
        migrations.AlterField(
            model_name='modelinfo',
            name='model_algo',
            field=models.CharField(choices=[('nvb', 'Naive Bayes'), ('svm', 'SVM'), ('knn', 'K-NN'), ('ann', 'Artificial Neural Networks')], default='knn', max_length=200),
        ),
        migrations.AlterField(
            model_name='modelinfo',
            name='model_up_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 3, 14, 7, 49, 47, 450280)),
        ),
    ]
