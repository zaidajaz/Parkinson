from django.db import models
from datetime import datetime
from django.contrib import auth
from django import forms
from .validators import validate_file_extension
from . import park_functions

class AlgoList(models.Model):
	algo_name = models.CharField(max_length=200)
	algo_display_name = models.CharField(max_length=200)

	def __str__(self):
		return self.algo_display_name

class DataInfo(models.Model):
	dataset_name = models.CharField(max_length=200)
	dataset_author = models.CharField(max_length=200)
	dataset_up_date = models.DateTimeField(default=datetime.now(), blank=True)
	dataset_desc = models.TextField()
	dataset_url = models.URLField(max_length=500)
	dataset_file = models.FileField(upload_to='datasets/', validators=[validate_file_extension])

	def __str__(self):
		return self.dataset_name

class ModelInfo(models.Model):
	model_name = models.CharField(max_length=200)
	model_author = models.CharField(max_length=200)
	model_up_date = models.DateTimeField(default=datetime.now(), blank=True)
	model_desc = models.TextField()
	model_algo = models.CharField(max_length=200)
	model_data_id = models.IntegerField()

	def __str__(self):
		return self.model_name