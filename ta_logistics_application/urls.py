from django.conf.urls import url
from . import views

app_name = 'ta_logic'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit/$', views.submit, name='submit')
]