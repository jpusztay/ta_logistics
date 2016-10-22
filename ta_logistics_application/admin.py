from django.contrib import admin
from .models import Students, Courses, Professors, ApplicationFields, CourseApplicants, StatusText

class StudentsAdmin(admin.ModelAdmin):
    model = Students

class CoursesAdmin(admin.ModelAdmin):
    model = Courses

class CourseApplicantsAdmin(admin.ModelAdmin):
    model = CourseApplicants

class ApplicationFieldsAdmin(admin.ModelAdmin):
    model = ApplicationFields

class StatusTextAdmin(admin.ModelAdmin):
    model = StatusText

class ProfessorsAdmin(admin.ModelAdmin):
    model = Professors

admin.site.register(ApplicationFields)
admin.site.register(Professors)
admin.site.register(Students)
admin.site.register(Courses)
admin.site.register(CourseApplicants)
admin.site.register(StatusText)
