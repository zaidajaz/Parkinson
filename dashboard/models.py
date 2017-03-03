from django.db import models

class DataInfo(models.Model):
	dataset_name = models.CharField(max_length=200)
	dataset_author = models.CharField(max_length=200)
	dataset_up_date = models.DateTimeField('Upload Date')
	dataset_desc = models.TextField()
	dataset_url = models.URLField(max_length=500)
	dataset_file = models.FileField(upload_to='datasets/')

	def __unicode__(self):
		return self.dataset_name