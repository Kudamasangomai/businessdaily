from django.contrib import admin
from .models import salestable
from company.models import comments
# Register your models here.
admin.site.register(salestable)
admin.site.register(comments)
