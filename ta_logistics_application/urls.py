from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^utalize/home/', views.group_index, name='home'),

    #Student
    url(r'^utalize/student/profile/$', views.student_profile, name='student_profile'),
    url(r'^utalize/student/$', views.student_index, name='student_index'),
    url(r'^utalize/student/class_list', views.student_class_list, name='student_class_list'),
    url(r'^utalize/student/application/$', views.student_application, name='student_application'),

    # Professor Context
    url(r'^utalize/professor/$', views.professor_index, name='professor_index'),
    url(r'^utalize/professor/create_class', views.professor_create_class, name='professor_create_class'),
    url(r'^utalize/professor/professor_class_applicants', views.professor_class_applicants, name='professor_class_applicants'),
    url(r'^utalize/professor/add_optional_field', views.add_optional_field, name='add_optional_field'),
    url(r'^utalize/professor/edit_optional_field', views.edit_optional_field, name='edit_optional_field'),
    url(r'^utalize/professor/view_optional_fields', views.view_optional_fields, name='view_optional_fields'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
