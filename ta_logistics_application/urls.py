from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^student/available_courses', views.available_courses, name='available_courses'),
    url(r'^student/application$', views.application, name='application'),
    url(r'^student/profile/$', views.student_profile, name='student_profile'),
    url(r'^student/profile/edit$', views.edit_student_profile, name='edit_student_profile'),
    url(r'^student/profile/create', views.create_student_account, name='create_student_account'),
    # Professor Context
    url(r'^professor/$', views.professor_index, name='professor_index'),
    url(r'^professor/create_course', views.professor_create_course, name='professor_create_course'),
    url(r'^professor/course_applicants', views.professor_course_applicants, name='professor_course_applicants'),

]
