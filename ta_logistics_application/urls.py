from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^home/', views.group_index, name='home'),

    # Student
    url(r'^student/profile/$', views.student_profile, name='student_profile'),
    url(r'^student/edit_profile/$', views.student_edit_profile, name='student_edit_profile'),
    url(r'^student/$', views.student_index, name='student_index'),
    url(r'^student/class_list', views.student_class_list, name='student_class_list'),
    url(r'^student/application/$', views.student_application, name='student_application'),
    url(r'^student/application/application_error$', views.application_error, name='application_error'),
    url(r'^student/payroll_info', views.payroll_info, name='payroll_info'),


    # Professor Context
    url(r'^professor/$', views.professor_index, name='professor_index'),
    url(r'^professor/create_class', views.professor_create_class, name='professor_create_class'),
    url(r'^professor/professor_class_applicants', views.professor_class_applicants, name='professor_class_applicants'),
    url(r'^professor/add_optional_field', views.add_optional_field, name='add_optional_field'),
    url(r'^professor/edit_optional_field', views.edit_optional_field, name='edit_optional_field'),
    url(r'^professor/view_optional_fields', views.view_optional_fields, name='view_optional_fields'),
    url(r'^professor/create_class_error', views.create_class_error, name='create_class_error'),


    # Admin Pages
url(r'^admin/payroll_registration', views.payroll_registration, name='payroll_registration'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)