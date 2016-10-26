from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^home/', views.group_index, name='home'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^student/profile/$', views.student_profile, name='student_profile'),
    url(r'^student/profile/edit$', views.edit_student_profile, name='edit_student_profile'),
]
