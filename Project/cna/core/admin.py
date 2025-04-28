from django.contrib import admin
from .models import User, CNA, ClientProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

admin.site.register(User)
admin.site.register(CNA)
admin.site.register(ClientProfile)

