from django.contrib import admin
from .models import Question, Captcha

admin.site.register(Question)
admin.site.register(Captcha)
