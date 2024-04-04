from django.contrib import admin
from .models import RecruiterData,Personality
from careers.models import *

# Register your models here.
admin.site.register(RecruiterData)
admin.site.register(Joblist)
admin.site.register(Personality)
