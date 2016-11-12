from django.contrib import admin
from .models import Students, Classes, Professors, ClassApplicants

class StudentsAdmin(admin.ModelAdmin):
    model = Students

class ClassesAdmin(admin.ModelAdmin):
    model = Classes

class ClassApplicantsAdmin(admin.ModelAdmin):
    model = ClassApplicants

#class ApplicationFieldsAdmin(admin.ModelAdmin):
#    model = ApplicationFields


class ProfessorsAdmin(admin.ModelAdmin):
    model = Professors

#admin.site.register(ApplicationFields)
admin.site.register(Professors)
admin.site.register(Students)
admin.site.register(Classes)
admin.site.register(ClassApplicants)
