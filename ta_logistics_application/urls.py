from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^home/', views.group_index, name='home'),
    url(r'^student/application/$', views.application, name='application'),
    url(r'^student/profile/$', views.student_profile, name='student_profile'),
    url(r'^student/profile/edit$', views.edit_student_profile, name='edit_student_profile'),
    url(r'^student/profile/create', views.create_student_account, name='create_student_account'),
    # Professor Context
    url(r'^professor/$', views.professor_index, name='professor_index'),
    url(r'^professor/create_class', views.professor_create_class, name='professor_create_class'),
    url(r'^professor/class_applicants', views.professor_class_applicants, name='professor_class_applicants'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)