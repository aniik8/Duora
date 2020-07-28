from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(question_data)
admin.site.register(answer_data)
admin.site.register(profile)