from django.contrib import admin
from budget.models import Category, Transaction, Budget

admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Budget)
