from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^home/', views.group_index, name='home'),

    #Student
    url(r'^student/index/$', views.student_index, name='student_index'),
    url(r'^student/apply/$', views.student_apply, name='student_apply'),
    url(r'^student/create', views.student_create, name='student_create'),
    url(r'^student/edit$', views.student_edit, name='student_edit'),

    # Professor Context
    url(r'^professor/$', views.professor_index, name='professor_index'),
    url(r'^professor/create_class', views.professor_create_class, name='professor_create_class'),

]
