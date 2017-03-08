from django.db import models
from datetime import datetime
from django.contrib import auth
from django import forms
from .validators import validate_file_extension

class DataInfo(models.Model):
	dataset_name = models.CharField(max_length=200)
	dataset_author = models.CharField(max_length=200)
	dataset_up_date = models.DateTimeField(default=datetime.now(), blank=True)
	dataset_desc = models.TextField()
	dataset_url = models.URLField(max_length=500)
	dataset_file = models.FileField(upload_to='datasets/', validators=[validate_file_extension])

	def __str__(self):
		return self.dataset_name