from django.contrib import admin
from .models import Students, Classes, Professors, ApplicationFields, ApplicationStatus, StatusText

class StudentsAdmin(admin.ModelAdmin):
    model = Students

class ClassesAdmin(admin.ModelAdmin):
    model = Classes

class ApplicationStatusAdmin(admin.ModelAdmin):
    model = ApplicationStatus

class ApplicationFieldsAdmin(admin.ModelAdmin):
    model = ApplicationFields

class StatusTextAdmin(admin.ModelAdmin):
    model = StatusText

class ProfessorsAdmin(admin.ModelAdmin):
    model = Professors

admin.site.register(ApplicationFields)
admin.site.register(Professors)
admin.site.register(Students)
admin.site.register(Classes)
admin.site.register(ApplicationStatus)
admin.site.register(StatusText)
