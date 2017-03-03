from django import forms
from .models import DataInfo

class DataUploadForm(forms.ModelForm):
	class Meta:
		model = DataInfo
		fields = ['dataset_name', 'dataset_author', 'dataset_up_date', 'dataset_desc', 'dataset_url', 'dataset_file']