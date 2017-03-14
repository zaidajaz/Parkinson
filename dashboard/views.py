
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from dashboard.forms import DataUploadForm, NewModelForm
from django.template import RequestContext
from django.http import HttpResponse
from datetime import datetime
from .models import DataInfo, ModelInfo

# Create your views here.

root_url = 'http://localhost:8000'

def dashboard(request):
	if request.user.id is None:
		return HttpResponseRedirect('/')

	return render_to_response('dashboard/dash_design.html', {'name':request.user.first_name + ' ' + request.user.last_name, 'root_url': root_url })

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
	return render_to_response('dashboard/model_list.html', args)

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
