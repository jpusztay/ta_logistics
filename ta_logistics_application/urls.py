from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^student/profile/$', views.student_profile, name='student_profile'),
    url(r'^student/profile/edit$', views.edit_student_profile, name='edit_student_profile'),
    url(r'^student/profile/create', views.create_student_account, name='create_student_account'),
]
