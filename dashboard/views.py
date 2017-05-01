
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from dashboard.forms import DataUploadForm, NewModelForm
from django.template import RequestContext
from django.http import HttpResponse
from datetime import datetime
from .models import DataInfo, ModelInfo, ModelConfig, ReportInfo, UserInfo
import csv
import os
from django.middleware import csrf
import json
from . import knn, svm, logistic_regression, naivebayes
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

	user_company = ''
	user_address = ''
	user_city = ''
	user_country = ''
	user_postal = 0
	user_desc = ''
	user_dp = ''
	user_fblink = ''
	user_twitterlink = ''
	user_gpluslink = ''
	user_data = UserInfo.objects.all().filter(user_id=request.user.id)
	for data in user_data:
		user_company = data.user_company
		user_address = data.user_address
		user_city = data.user_address_city
		user_country = data.user_address_country
		user_postal = data.user_address_pin
		user_desc = data.user_desc
		user_dp = data.user_profile_pic.name
		user_fblink = data.user_fblink
		user_twitterlink = data.user_twitterlink
		user_gpluslink = data.user_gpluslink 
	
	user_dp = user_dp.split('/')
	dp_file_name = user_dp[-1]
	user_args = {"root_url":root_url, "user_username":request.user.username, "user_firstname":request.user.first_name, "user_lastname":request.user.last_name, "name":request.user.first_name + ' ' + request.user.last_name, "user_email":request.user.email , "user_company":user_company, "user_address":user_address, "user_city":user_city, "user_country":user_country, "user_postal":user_postal, "user_desc":user_desc, "user_fblink":user_fblink, "user_twitterlink":user_twitterlink, "user_gpluslink":user_gpluslink, "user_dp":dp_file_name}

	return render(request, 'dashboard/user.html', user_args)

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

def dataDetails(request):
	if request.user.id is None:
		return HttpResponseRedirect('/')

	if request.GET:
		data_id = request.GET.get('id', -1)
		if int(data_id) > -1:
			data_list = DataInfo.objects.all().filter(id=data_id)
			name = ''
			author = ''
			date = datetime.now()
			desc = ''
			url = ''

			for data in data_list:
				name = data.dataset_name
				author = data.dataset_author
				date = data.dataset_up_date
				desc = data.dataset_desc
				url = data.dataset_url
			args = {'name':name,'author':author,'date':date,'desc':desc,'url':url}
			return render(request,'dashboard/data_details_layout.html', args)
		else:
			return HttpResponse("Invalid Request")
	else:
		return HttpResponse("Invalid Request")

def model_list(request):
	if request.user.id is None:
		return HttpResponseRedirect('/')

	all_entries  = ModelInfo.objects.all().filter(model_author=request.user.username).order_by('-model_up_date')
	args = {'name':request.user.first_name + ' ' + request.user.last_name, 'root_url':root_url }
	args['model_list'] = all_entries
	args['csrf_for_config'] = csrf.get_token(request)
	return render_to_response('dashboard/model_list.html', args)

def modelDetails(request):
	if request.user.id is None:
		return HttpResponseRedirect('/')

	if request.GET:
		model_id = request.GET.get('id', -1)
		if int(model_id) > -1:
			model_list = ModelInfo.objects.all().filter(id=model_id)
			name = ''
			author = ''
			date = datetime.now()
			desc = ''
			algo = ''

			for model in model_list:
				name = model.model_name
				author = model.model_author
				date = model.model_up_date
				desc = model.model_desc
				algo = model.model_algo
			args = {'name':name,'author':author,'date':date,'desc':desc, 'algo_used': algo}
			return render(request,'dashboard/model_details_layout.html', args)
		else:
			return HttpResponse("Invalid Request")
	else:
		return HttpResponse("Invalid Request")

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
 		model_algo = ''
 		data_id = 0
 		for model in model_set:
 			model_name = model.model_name
 			data_id = model.model_data_id
 			model_algo = model.model_algo
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
 		metrics = {}

 		if model_algo == 'nvb':
 			metrics = (naivebayes.calc_accuracy(fileFullName, insig_field, class_field))
 		if model_algo == 'knn':
 			metrics = (knn.calc_accuracy(fileFullName, insig_field, class_field))
 		if model_algo == 'svm':
 			metrics = (svm.calc_accuracy(fileFullName, insig_field, class_field))
 		if model_algo == 'logistic_regression':
 			metrics = (logistic_regression.calc_accuracy(fileFullName, insig_field, class_field))

 		report_list = ReportInfo.objects.all().filter(report_model_id=model_id)
 		reportExists = False
 		for report in report_list:
 			reportExists = True

 		if reportExists:
 			newReport = ReportInfo.objects.get(report_model_id=model_id)
 			newReport.report_name = report_name
 			newReport.report_author = request.user.username
 			newReport.report_up_date = datetime.now()
 			newReport.report_accuracy = metrics["classification_accuracy"]
 			newReport.report_model_id = model_id
 			newReport.report_class_error = metrics["classification_error"]
 			newReport.report_conf_matrix = metrics["confusion_matrix"]
 			newReport.save()
 		else:
 			newReport = ReportInfo()
 			newReport.report_name = report_name
 			newReport.report_author = request.user.username
 			newReport.report_up_date = datetime.now()
 			newReport.report_accuracy = metrics["classification_accuracy"]
 			newReport.report_model_id = model_id
 			newReport.report_class_error = metrics["classification_error"]
 			newReport.report_conf_matrix = metrics["confusion_matrix"]
 			newReport.save()

 		return HttpResponse(str(metrics))

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
	report_class_error = 0
	report_conf_matrix = ''


	if int(report_id) > -1:
		report_details = ReportInfo.objects.all().filter(id=report_id)
		for report in report_details:
			report_name = report.report_name
			report_author = report.report_author
			report_date = report.report_up_date
			model_id = report.report_model_id
			report_accuracy = report.report_accuracy
			report_class_error = report.report_class_error
			report_conf_matrix = report.report_conf_matrix

		model_details = ModelInfo.objects.all().filter(id=model_id)
		for model in model_details:
			algo_used = model.model_algo
			dataset_id = model.model_data_id

		data_details = DataInfo.objects.all().filter(id=dataset_id)
		for data in data_details:
			dataset_name = data.dataset_name

		report_conf_matrix = report_conf_matrix.replace('[','').replace(']','').replace('\n','')
		report_conf_matrix = report_conf_matrix.replace(' ',',')
		report_conf_matrix = report_conf_matrix.split(',')
			

		element_list = []
		for element in report_conf_matrix:
			if element:
				element_list.append(element)

		report_conf_matrix = element_list
		conf_up_1 = report_conf_matrix[0]
		conf_up_2 = report_conf_matrix[1]
		conf_down_1 = report_conf_matrix[2]
		conf_down_2 = report_conf_matrix[3]
		

		data_args = {"report_name":report_name,"report_author":report_author,"report_date":report_date,"algo_used":algo_used,"dataset_name":dataset_name,"report_id":report_id,"report_accuracy":report_accuracy, "report_class_error":report_class_error, "report_conf_matrix":report_conf_matrix, "cu1":conf_up_1, "cu2":conf_up_2, "du1": conf_down_1, "du2": conf_down_2}
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