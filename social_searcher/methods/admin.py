from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import MethodResult


admin.site.register(MethodResult, ModelAdmin)
