from django import forms
from .models import DataInfo

class DataUploadForm(forms.ModelForm):
	class Meta:
		model = DataInfo
		fields = ['dataset_name', 'dataset_author', 'dataset_up_date', 'dataset_desc', 'dataset_url', 'dataset_file']
		widgets = {
            'dataset_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dataset_desc': forms.Textarea(attrs={'class': 'form-control'}),
            
            'dataset_url': forms.TextInput(attrs={'class': 'form-control'}),
           # 'dataset_file': forms.FileInput(attrs={'class': 'form-control'}),
        }