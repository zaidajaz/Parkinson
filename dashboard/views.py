
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from dashboard.forms import DataUploadForm, NewModelForm
from django.template import RequestContext
from django.http import HttpResponse
from datetime import datetime
from .models import DataInfo, ModelInfo, ModelConfig, ReportInfo
import csv
import os
from django.middleware import csrf
import json
# Create your views here.

root_url = 'http://localhost:8000'

def dashboard(request):
	if request.user.id is None:
		return HttpResponseRedirect('/')

	data_list = DataInfo.objects.all().filter(dataset_author=request.user.username).order_by('-dataset_up_date')[0:3]
	model_list = ModelInfo.objects.all().filter(model_author=request.user.username).order_by('-model_up_date')[0:3]
	args = {'name':request.user.first_name + ' ' + request.user.last_name, 'root_url': root_url }
	args['dataset_list'] = data_list
	args['model_list'] = model_list
	return render_to_response('dashboard/dash_design.html', args)

def user_profile(request):

	if request.user.id is None:
		return HttpResponseRedirect('/')

	return render_to_response('dashboard/user.html', {'name':request.user.first_name + ' ' + request.user.last_name, 'root_url':root_url })

def data_list(request):

	if request.user.id is None:
		return HttpResponseRedirect('/')

	all_entries  = DataInfo.objects.all().filter(dataset_author=request.user.username).order_by('-dataset_up_date')
	args = {'name':request.user.first_name + ' ' + request.user.last_name, 'root_url':root_url }
	args['data_list'] = all_entries
	return render_to_response('dashboard/data_list.html', args)

def newData(request):

	if request.user.id is None:
		return HttpResponseRedirect('/')

	if request.POST:
		 form = DataUploadForm(request.POST, request.FILES)
		 if form.is_valid():
		 	form.save()
		 	return HttpResponseRedirect('/dashboard/datasets/')
		 return HttpResponse(form.errors.as_json())
	else:
		date = datetime.now()
		form = DataUploadForm()
		args = {'name':request.user.first_name + ' ' + request.user.last_name, 'root_url':root_url }
		args['form'] = form
		args['date'] = date
		args['userObj'] = request.user
		return render(request, 'dashboard/newData.html', args)

def model_list(request):
	if request.user.id is None:
		return HttpResponseRedirect('/')

	all_entries  = ModelInfo.objects.all().filter(model_author=request.user.username).order_by('-model_up_date')
	args = {'name':request.user.first_name + ' ' + request.user.last_name, 'root_url':root_url }
	args['model_list'] = all_entries
	args['csrf_for_config'] = csrf.get_token(request)
	return render_to_response('dashboard/model_list.html', args)

def report_list(request):
	if request.user.id is None:
		return HttpResponseRedirect('/')

	all_entries  = ReportInfo.objects.all().filter(report_author=request.user.username).order_by('-report_up_date')
	args = {'name':request.user.first_name + ' ' + request.user.last_name, 'root_url':root_url }
	args['report_list'] = all_entries
	return render_to_response('dashboard/report_list.html', args)				

def newModel(request):

	if request.user.id is None:
		return HttpResponseRedirect('/')

	if request.POST:
		 form = NewModelForm(request.POST)
		 if form.is_valid():
		 	form.save()
		 	return HttpResponseRedirect('/dashboard/models/')
		 return HttpResponse(form.errors.as_json())
	else:
		date = datetime.now()
		form = NewModelForm()
		data_list  = DataInfo.objects.all().filter(dataset_author=request.user.username).order_by('-dataset_up_date')
		args = {'name':request.user.first_name + ' ' + request.user.last_name, 'root_url':root_url }
		args['form'] = form
		args['date'] = date
		args['userObj'] = request.user
		args['data_list'] = data_list
		return render(request, 'dashboard/newModel.html', args)

def modelConfig(request):
	if request.user.id is None:
		return HttpResponseRedirect('/')

	if request.POST:

		data = request.POST.get('post_data')
		jsonData = json.loads(data)

		insig_field = jsonData['insig']
		class_field = jsonData['class']
		model_id = int(jsonData['model_id'])

		newConfig = ModelConfig.objects.get(model_id=model_id)
		newConfig.model_insig_cols = insig_field
		newConfig.model_classifier = class_field
		newConfig.model_id = model_id
		newConfig.save()

		return HttpResponse('Success!')

	modelID = request.GET.get('id', -1)
	if int(modelID) > -1:
		modelObjs = ModelInfo.objects.all().filter(id=modelID)
		for modelobj in modelObjs:
			dataID = modelobj.model_data_id

		dataObjs = DataInfo.objects.all().filter(id=dataID)
		for dataobj in dataObjs:
			filename = dataobj.dataset_file.name
			fileLoc = os.path.dirname(os.path.abspath(filename))
			filename = filename.split('/')

			rows = ''

			fileFullName = str(fileLoc) + '/' + str(filename[-1])
			output = ''
			with open(fileFullName) as f:
				reader = csv.reader(f)
				for row in reader:
					rows = rows + '<br>' + str(row)
					break

		args = {'col_list':row}
			 					 
		return render(request, 'dashboard/configure_template.html', args)
	else:
		return HttpResponse('Invalid Request')