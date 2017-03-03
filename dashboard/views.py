from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from dashboard.forms import DataUploadForm
from django.template import RequestContext
from django.http import HttpResponse

# Create your views here.

root_url = 'http://localhost:8000'

def dashboard(request):
	if request.user.id is None:
		return HttpResponseRedirect('/')

	return render_to_response('dashboard/dash_design.html', {'name':request.user.first_name + ' ' + request.user.last_name, 'root_url': root_url })

def user_profile(request):
	return render_to_response('dashboard/user.html', {'name':request.user.first_name + ' ' + request.user.last_name, 'root_url':root_url })

def data_list(request):
	return render_to_response('dashboard/data_list.html', {'name':request.user.first_name + ' ' + request.user.last_name, 'root_url':root_url })

def newData(request):
	if request.POST:
		 form = DataUploadForm(request.POST)
		 if form.is_valid():
		 	form.save()
		 	return HttpResponseRedirect('/dashboard/datasets/')
		 return HttpResponse('Form Input invalid')
	else:
		form = DataUploadForm()
		args = {'name':request.user.first_name + ' ' + request.user.last_name, 'root_url':root_url }
		args['form'] = form
		return render(request, 'dashboard/newData.html', args)


