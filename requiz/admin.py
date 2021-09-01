from django.contrib import admin

from .models import KidUser, AdultUser, Question, Option

admin.site.register(KidUser)

admin.site.register(AdultUser)

admin.site.register(Question)

admin.site.register(Option)

# Register your models here.
