from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^home/', views.group_index, name='home'),

    #Student
    url(r'^student/profile/$', views.student_profile, name='student_profile'),
    url(r'^student/status/$', views.student_status, name='student_status'),
    url(r'^student/class_list/$', views.student_class_list, name='student_class_list'),
    url(r'^student/application/$', views.student_application, name='student_application'),

    # Professor Context
    url(r'^professor/$', views.professor_index, name='professor_index'),
    url(r'^professor/create_class', views.professor_create_class, name='professor_create_class'),

]
