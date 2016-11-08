from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^home/', views.group_index, name='home'),

    #Student
    url(r'^student/profile$', views.student_index, name='student_profile'),
    url(r'^student/apply/$', views.student_apply, name='student_apply'),
    url(r'^student/create', views.student_create, name='student_create'),
    url(r'^student/edit$', views.student_edit, name='student_edit'),

    # Professor Context
    url(r'^professor/$', views.professor_index, name='professor_index'),
    url(r'^professor/create_class', views.professor_create_class, name='professor_create_class'),
    url(r'^professor/professor_class_applicants', views.professor_class_applicants, name='professor_class_applicants'),
    url(r'^professor/add_optional_field', views.add_optional_field, name='add_optional_field'),
    url(r'^professor/edit_optional_field', views.edit_optional_field, name='edit_optional_field'),
    url(r'^professor/view_optional_fields', views.view_optional_fields, name='view_optional_fields'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)