from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
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
