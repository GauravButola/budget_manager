from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	category_name = models.CharField(max_length=50)
	spent = models.BooleanField(default=True)

	def __unicode__(self):
		return self.category_name

class Transaction(models.Model):
	user = models.ForeignKey(User)
	category = models.ForeignKey(Category)
	comment = models.CharField(max_length=50)
	amount = models.DecimalField(max_digits=20, decimal_places=3)
	date = models.DateField(auto_now_add=True)

	date.editable = True

	def __unicode__(self):
		return self.comment

class Budget(models.Model):
	user = models.ForeignKey(User)
	amount = models.DecimalField(max_digits=20, decimal_places=3)
	balance = models.DecimalField(max_digits=20, decimal_places=3)
	period = models.DateField(auto_now_add=True)

	period.editable = True

	def __unicode__(self):
		return str(self.user) + " " + str(self.period)

