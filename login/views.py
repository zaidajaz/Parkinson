from django.shortcuts import render, render_to_response, redirect
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth


# Create your views here.

def login(request):	
	if request.user.id is not None:
		return HttpResponseRedirect('/dashboard/')

	invalid = request.GET.get('invalid', 0)
	return render(request, 'login/loginbody.html', {'invalid':invalid})

def login_auth(request):
	if request.POST:
		username = password = ''
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth.login(request, user)
				return HttpResponseRedirect('/dashboard/')
			else:
				return HttpResponse('<p>User Inactive!</p>')
		else:
			return HttpResponseRedirect('/?invalid=1', {'invalid':1})

	return HttpResponseRedirect('/')

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')




	