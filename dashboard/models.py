from django.db import models
from datetime import datetime
from django.contrib import auth
from django import forms
from .validators import validate_file_extension, validate_user_dp_extension
from . import park_functions
import os

class UserInfo(models.Model):
	user_id = models.IntegerField()
	user_company = models.CharField(max_length=200)
	user_address = models.TextField()
	user_address_city = models.CharField(max_length=200)
	user_address_country = models.CharField(max_length=200)
	user_address_pin = models.IntegerField()
	user_desc = models.CharField(max_length=160)
	user_profile_pic = models.FileField(upload_to='dashboard/static/img/userprofiles/', validators=[validate_user_dp_extension])
	user_fblink = models.URLField()
	user_twitterlink = models.URLField()
	user_gpluslink = models.URLField()
	def __str__(self):
		return str(self.user_id)


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

	def extension(self):
		name, extension = os.path.splitext(self.dataset_file.name)
		return extension

class ModelInfo(models.Model):
	model_name = models.CharField(max_length=200)
	model_author = models.CharField(max_length=200)
	model_up_date = models.DateTimeField(default=datetime.now(), blank=True)
	model_desc = models.TextField()
	model_algo = models.CharField(max_length=200)
	model_data_id = models.IntegerField()

	def __str__(self):
		return self.model_name

class ModelConfig(models.Model):
	model_id = models.IntegerField()
	model_insig_cols = models.CharField(max_length=1000)
	model_classifier = models.CharField(max_length=100)

	def __str__(self):
		return self.model_classifier

class ReportInfo(models.Model):
	report_name = models.CharField(max_length=200)
	report_author = models.CharField(max_length=200)
	report_up_date = models.DateTimeField(default=datetime.now(), blank=True)
	report_model_id = models.IntegerField()
	report_accuracy = models.IntegerField()

	def __str__(self):
		return self.report_name