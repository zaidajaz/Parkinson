
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
from . import knn
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

def newReport(request):
 	if request.user.id is None:
 		return HttpResponseRedirect('/')

 	#modelid

 	model_id = request.GET.get('id',-1)
 	if int(model_id) > -1:
 		model_set = ModelInfo.objects.all().filter(id=model_id)
 		model_name = ''
 		data_id = 0
 		for model in model_set:
 			model_name = model.model_name
 			data_id = model.model_data_id
 			break

 		data_set = DataInfo.objects.all().filter(id=data_id)
 		filename = ''
 		for data in data_set:
 			filename = data.dataset_file.name
 			break

 		fileLoc = os.path.dirname(os.path.abspath(filename))
 		filename = filename.split('/')
 		fileFullName = str(fileLoc) + '/' + str(filename[-1])
 		report_name = '[Report] - ' + str(model_name)

 		#Reading Configuration Data
 		config_list = ModelConfig.objects.all().filter(model_id=model_id)
 		insig_field = ''
 		class_field = ''
 		for config in config_list:
 			insig_field = config.model_insig_cols
 			class_field = config.model_classifier

 		accuracy = int(knn.calc_accuracy(fileFullName, insig_field, class_field) * 100)

 		report_list = ReportInfo.objects.all().filter(report_model_id=model_id)
 		reportExists = False
 		for report in report_list:
 			reportExists = True

 		if reportExists:
 			newReport = ReportInfo.objects.get(report_model_id=model_id)
 			newReport.report_name = report_name
 			newReport.report_author = request.user.username
 			newReport.report_up_date = datetime.now()
 			newReport.report_accuracy = accuracy
 			newReport.report_model_id = model_id
 			newReport.save()
 		else:
 			newReport = ReportInfo()
 			newReport.report_name = report_name
 			newReport.report_author = request.user.username
 			newReport.report_up_date = datetime.now()
 			newReport.report_accuracy = accuracy
 			newReport.report_model_id = model_id
 			newReport.save()

 		return HttpResponse(str(accuracy))

		#Save report data to databse

 	return HttpResponse("Invalid Request")

# 	if request.POST:
# 		 form = NewModelForm(request.POST)
# 		 if form.is_valid():
# 		 	form.save()
# 		 	return HttpResponseRedirect('/dashboard/models/')
# 		 return HttpResponse(form.errors.as_json())
# 	else:
# 		date = datetime.now()
# 		form = NewModelForm()
# 		data_list  = DataInfo.objects.all().filter(dataset_author=request.user.username).order_by('-dataset_up_date')
# 		args = {'name':request.user.first_name + ' ' + request.user.last_name, 'root_url':root_url }
# 		args['form'] = form
# 		args['date'] = date
# 		args['userObj'] = request.user
# 		args['data_list'] = data_list
# 		return render(request, 'dashboard/newModel.html', args)


def viewReport(request):
	if request.user.id is None:
		return HttpResponseRedirect('/')

	report_id = request.GET.get('id',-1)
	report_name = ''
	report_author = ''
	report_date = ''
	model_id = 0
	algo_used = ''
	dataset_id = 0
	dataset_name = ''
	report_accuracy = 0

	if int(report_id) > -1:
		report_details = ReportInfo.objects.all().filter(id=report_id)
		for report in report_details:
			report_name = report.report_name
			report_author = report.report_author
			report_date = report.report_up_date
			model_id = report.report_model_id
			report_accuracy = report.report_accuracy

		model_details = ModelInfo.objects.all().filter(id=model_id)
		for model in model_details:
			algo_used = model.model_algo
			dataset_id = model.model_data_id

		data_details = DataInfo.objects.all().filter(id=dataset_id)
		for data in data_details:
			dataset_name = data.dataset_name

		data_args = {"report_name":report_name,"report_author":report_author,"report_date":report_date,"algo_used":algo_used,"dataset_name":dataset_name,"report_id":report_id,"report_accuracy":report_accuracy}
		return render(request, 'dashboard/report_template.html', data_args)
	else:
		return render(request, 'dashboard/css-circles.html')



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

		config_list = ModelConfig.objects.all().filter(model_id=model_id)
		configExists = False
		for config in config_list:
			configExists = True

		if configExists:
			newConfig = ModelConfig.objects.get(model_id=model_id)
			newConfig.model_insig_cols = insig_field
			newConfig.model_classifier = class_field
			newConfig.model_id = model_id
			newConfig.save()
		else:
			newConfig = ModelConfig()
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



def predict(request):
	if request.user.id is None:
		return HttpResponseRedirect('/')

	if request.POST:
		post_values = request.POST.get('a') + ',' + request.POST.get('b') + ',' + request.POST.get('c') + ',' + request.POST.get('d')+ ',' + request.POST.get('e') + ',' + request.POST.get('f') + ',' + request.POST.get('g') + ',' + request.POST.get('h') + ',' + request.POST.get('i') + ',' + request.POST.get('j') + ',' + request.POST.get('k') + ',' + request.POST.get('l') + ',' + request.POST.get('m') + ',' + request.POST.get('n') + ',' + request.POST.get('o') + ',' + request.POST.get('p') + ',' + request.POST.get('q') + ',' + request.POST.get('r') + ',' + request.POST.get('s') + ',' + request.POST.get('t') + ',' + request.POST.get('u') + ',' + request.POST.get('v')
		result = knn.predict(str(post_values))
		args = {'name':request.user.first_name + ' ' + request.user.last_name, 'root_url':root_url }
		args['class_predicted'] = result
		return render(request, 'dashboard/predict_outcome.html', args)

	args = {'name':request.user.first_name + ' ' + request.user.last_name, 'root_url':root_url }
	return render(request, 'dashboard/predict.html', args)	