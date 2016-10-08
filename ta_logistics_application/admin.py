from django.contrib import admin
from .models import Application, Classes

#class ApplicationAdmin(admin.ModelAdmin):
    #model = Application

#class OpenClassAdmin(admin.ModelAdmin):
    #model = OpenClass

admin.site.register(Classes)
admin.site.register(Application)