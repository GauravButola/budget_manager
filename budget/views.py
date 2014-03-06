from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm

def home(request):
	return render(request, 'budget/home.html')

def login(request):
	return HttpResponse("Login here")

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/login/')

	args = {}
	args.update(csrf(request))

	args['form'] = UserCreationForm()
	return render_to_response('budget/register.html', args)

