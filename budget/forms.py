from budget.models import *
from django.forms import ModelForm, Select
from django import forms

class TransactionForm(ModelForm):
	class Meta:
		model = Transaction
		fields = ['amount', 'category', 'comment']

