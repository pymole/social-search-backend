from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username', 'password', 'vk_token']


admin.site.register(User, CustomUserAdmin)
