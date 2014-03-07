from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from budget.forms import *
from datetime import date
from decimal import Decimal

def index(request):
	if request.user.is_authenticated():
			return HttpResponseRedirect('/home/')
	return render(request, 'budget/index.html')

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
	"""
	If user doesn't have this months budget data, then create one, with
	budget amount as Null and balance copied from last month.
	"""
	user = request.user
	user_budgets = Budget.objects.filter(user=user)
	if not user_budgets:
		Budget.objects.create(user=user, balance=0)
	last_month_budget = user_budgets.last()
	today = date.today() 
	curr_month_year = today.strftime('%Y %m')
	last_budget_month_year = last_month_budget.period.strftime('%Y %m')

	if last_budget_month_year != curr_month_year:
		"""If there's no budget for current month"""
		Budget.objects.create(user=user, balance=last_month_budget.balance)
	
	return render(request, 'budget/home.html')

@login_required
def transactions(request):
	"""
	Sets different categories for credit and debit forms by passing 
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
	
	"""
	Show budget warning, if balance is less than budget amount
	"""
	budget = Budget.objects.get(user=request.user)	
	if budget.balance < budget.amount:
		args['budget_warning'] = "You have gone past your budget for this month"
	return render(request, 'budget/transactions.html', args)

def handle_transaction(request, form, tr_method):
	transaction = form.save(commit=False)
	transaction.user = request.user
	transaction.save()

	user = request.user
	user_budgets = Budget.objects.filter(user=user)
	budget = user_budgets.last()
	if tr_method == 'credit':
		#Increase user's balance
		budget.balance += Decimal(form.data['amount'])
	elif tr_method == 'debit':
		#Deduct user's balance
		budget.balance -= Decimal(form.data['amount'])
	budget.save()

@login_required
def credit(request):
	form = TransactionForm(request.POST)
	if form.is_valid():
		if request.method == 'POST':
			handle_transaction(request, form, 'credit')
		return HttpResponseRedirect('/transactions/')
	else:
		return HttpResponse("Form validation error, please check the data you entered")

@login_required
def debit(request):
	form = TransactionForm(request.POST)
	if form.is_valid():
		if request.method == 'POST':
			handle_transaction(request, form, 'debit')
		return HttpResponseRedirect('/transactions/')
	else:
		return HttpResponse("Form validation error, please check the data you entered")

@login_required
def budget(request):
	args = {}
	#POST request to change current months budget
	if request.method == 'POST':
		form = BudgetForm(request.POST)
		if form.is_valid():
			user = request.user
			user_budgets = Budget.objects.filter(user=user)
			budget = user_budgets.last()
			budget.amount = Decimal(form.data['amount'])
			budget.save()
			return HttpResponseRedirect('/budget/')
		else:
			args['error'] = "Invalid data entered"
	args['form'] = BudgetForm()
	user = request.user
	user_budgets = Budget.objects.filter(user=user)
	args['budget'] = user_budgets.last()

	today = date.today() 
	curr_month = today.strftime('%m')
	credit_transactions = Transaction.objects.filter(user=user, category__spent=False, date__month=curr_month)
	debit_transactions = Transaction.objects.filter(user=user, category__spent=True, date__month=curr_month)
	args['credit'] = args['debit'] = 0
	for transaction in credit_transactions:
		args['credit'] += transaction.amount 
	for transaction in debit_transactions:
		args['debit'] += transaction.amount 
	return render(request, 'budget/budget.html', args)

@login_required
def categories(request):
	args = {}
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/categories/')
		else:
			args['error'] = "Invalid data entered"
	args['form'] = CategoryForm()

	args['curr_month_credit'] = Category.objects.filter(spent=False)
	args['curr_month_debit'] = Category.objects.filter(spent=True)
	return render(request, 'budget/categories.html', args)

