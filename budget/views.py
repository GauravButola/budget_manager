from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	return render(request, 'budget/home.html')

def login(request):
	return HttpResponse("Login here")

def register(request):
	return HttpResponse("Register here")
