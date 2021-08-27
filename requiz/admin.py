from django.contrib import admin

from .models import KidUser, AdultUser, Query

admin.site.register(KidUser)

admin.site.register(AdultUser)

admin.site.register(Query)

# Register your models here.
