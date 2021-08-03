from django.contrib import admin

# Register your models here.
from .models import accounts, months

admin.site.register(accounts)
admin.site.register(months)
