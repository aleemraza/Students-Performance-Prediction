from django.contrib import admin
from .models import StudentResults
from .models import UserProfile

# Register your models here.

admin.site.register(StudentResults)
admin.site.register(UserProfile)