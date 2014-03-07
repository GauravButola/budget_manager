from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from budget.forms import *

def index(request):
	if request.user.is_authenticated():
			return HttpResponseRedirect('/home/')
	return render(request, 'budget/index.html')

def error(request):
	return render(request, 'budget/error.html')

def login(request):
	if request.user.is_authenticated():
			return HttpResponseRedirect('/home/')

	args = {}
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			#Found user
			auth_login(request, user)
			return HttpResponseRedirect('/home/')
		else:
			args['error'] = "Found error"
	return render(request, 'budget/login.html', args)

def logout(request):
	auth_logout(request)
	return HttpResponseRedirect('/')

def register(request):
	if request.user.is_authenticated():
			return HttpResponseRedirect('/home/')

	args = {}
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/login/')
		else:
			args['error'] = "Found errors"
	args.update(csrf(request))
	args['form'] = UserCreationForm()
	return render(request, 'budget/register.html', args)

@login_required
def home(request):
	return render(request, 'budget/home.html')

def transactions(request):
	"""
	Sets different categories for credi and debit forms by passing 
	different queryset and finally passing a queryset to the form
	class so that validations don't fail.
	"""
	args = {}
  #Only show categories of earnings
	creditQset = Category.objects.filter(spent=False)
	TransactionForm.base_fields['category'] = forms.ModelChoiceField(queryset=creditQset)
	args['creditform'] = TransactionForm()
	
  #Only show categories of spendings
	debitQset = Category.objects.filter(spent=True)
	TransactionForm.base_fields['category'] = forms.ModelChoiceField(queryset=debitQset)

	args['debitform'] = TransactionForm()
	
  #Finally, making all Category objects available
	qset = Category.objects.all()
	TransactionForm.base_fields['category'] = forms.ModelChoiceField(queryset=qset)
	return render(request, 'budget/transactions.html', args)

def credit(request):
	args = {}
	if request.method == 'POST':
		form = TransactionForm(request.POST)
		transaction = form.save(commit=False)
		transaction.user = request.user
		transaction.save()
		# Fixme
		# Add to user balance too
		
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/transactions/')
		else:
			return HttpResponseRedirect('/home/')

def debit(request):
	args = {}
	if request.method == 'POST':
		form = TransactionForm(request.POST)
		transaction = form.save(commit=False)
		transaction.user = request.user
		transaction.save()
		# Fixme
		# deduct user balance too
		
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/transactions/')
		else:
			return HttpResponseRedirect('/home/')
