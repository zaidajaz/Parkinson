from django import forms
from .models import DataInfo, ModelInfo, AlgoList

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

class NewModelForm(forms.ModelForm):
    class Meta:
        CHOICES = AlgoList.objects.all()
        model = ModelInfo
        fields = ['model_name', 'model_author', 'model_up_date', 'model_desc', 'model_algo', 'model_data_id']
        widgets = {
            'model_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_author': forms.TextInput(attrs={'class': 'form-control'}),
            'model_desc': forms.Textarea(attrs={'class': 'form-control'}),
            'model_algo': forms.Select(attrs={'class': 'form-control'}, choices=(( (x.algo_name, x.algo_display_name) ) for x in CHOICES)),
            'model_data_id': forms.NumberInput(attrs={'class':'form-control cust-data-id'}),
           # 'dataset_file': forms.FileInput(attrs={'class': 'form-control'}),
        }


