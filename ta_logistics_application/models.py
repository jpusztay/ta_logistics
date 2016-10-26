from django.db import models

# the following lines added:
import datetime
from django.utils import timezone


class Students(models.Model):
    applying_class = models.CharField(max_length=6)
    ubit_name = models.CharField(max_length=10)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gpa = models.FloatField()
    class_grade = models.CharField(max_length=2)
    resume_url = models.URLField()


class Classes(models.Model):
    professor_ubit = models.CharField(max_length=10)
    professor_first_name = models.CharField(max_length=30)
    professor_last_name = models.CharField(max_length=30)
    available_hours = models.IntegerField()


class Professors(models.Model):
    ubit_name = models.CharField(max_length=10)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)


class ApplicationParameters(models.Model):
    field_name = models.CharField(max_length=30)
    is_default = models.BooleanField()
    data_type = models.CharField(max_length=6)
    max_length = models.IntegerField()


class Resume(models.Model):
    document = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

