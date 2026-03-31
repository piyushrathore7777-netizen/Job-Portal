from django.contrib import admin
from .models import Company,Job
from .models import Apply
# Register your models here.
admin.site.register(Apply)
admin.site.register(Company)
admin.site.register(Job)