from django.contrib import admin
from .models import Students, Classes, Professors, ApplicationParameters, Resume

class ApplicationParametersAdmin(admin.ModelAdmin):
    model = ApplicationParameters

class ProfessorsAdmin(admin.ModelAdmin):
    model = Professors

admin.site.register(ApplicationParameters)
admin.site.register(Professors)