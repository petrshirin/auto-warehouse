from django.contrib import admin
from .models import UserProfile, UserRegistrationCode

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserRegistrationCode)

