from django.db import models
from django.core.validators import validate_comma_separated_integer_list, MaxValueValidator, MinValueValidator
# the following lines added:
import datetime
from django.utils import timezone
from ta_logistics_application.validators import validate_optional_field_json


class DataDefinitions:
    GPA_CHOICES = (
        (4.0, '4.0'),
        (3.9, '3.9'),
        (3.8, '3.8'),
        (3.7, '3.7'),
        (3.6, '3.6'),
        (3.5, '3.5'),
        (3.4, '3.4'),
        (3.3, '3.3'),
        (3.2, '3.2'),
        (3.1, '3.1'),
        (3.0, '3.0'),
        (-1, '< 3.0'),
    )

    GRADE_CHOICES = (
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('> C-', '> C-'),
    )
    FIELD_TYPE_CHOICES = (
        ('TEXT', 'Text String'),
        ('INT', 'Integer Number'),
        ('REAL', 'Decimal Number'),
    )

    COMFORT_LVLS = (
        ('Expert','Expert'),
        ('Advanced','Advanced'),
        ('Moderate','Moderate'),
        ('Novince','Novince'),
        ('None','None'),
    )

    INT_FIELD = "INT"
    FLOAT_FIELD = "FLOAT"
    TEXT_FIELD = "TEXT"
    COMFORT_LVL_FIELD = "CMFT"

    def getActiveSemesters(self):
        ret = []
        curYear = datetime.date.today().year
        for i in range(curYear, curYear + 3):
            ret.append(('FA' + str(i)[-2:], 'Fall ' + str(i)))
            ret.append(('SP' + str(i)[-2:], 'Spring ' + str(i)))
        return tuple(ret)

    def getOptionalFields(self):
        ret = []
        for i in ApplicationFields.objects.filter(is_default=False):
            ret.append((i.id, i.field_text))
        return tuple(ret)


class Students(models.Model):
    ubit_name = models.CharField(max_length=10)
    person_number = models.CharField(max_length=8)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gpa = models.FloatField(choices=DataDefinitions.GPA_CHOICES)
    resume = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    teaching_experience = models.CharField(max_length=400, default="")

class Classes(models.Model):
    #Professor ID: Linked to auto incremented ID of professor table
    professor_id = models.IntegerField()
    active_semester = models.CharField(max_length=4)
    # This would hold 'CSE442' or what ever
    class_listing_id = models.CharField(max_length=6)
    class_name = models.CharField(max_length=50)
    available_hours = models.IntegerField()
    selected_optional_field_ids = models.CharField(max_length = 200, validators=[validate_comma_separated_integer_list], null=True)

class ClassApplicants(models.Model):
    #Linked to auto incremented ID of classes table
    class_id = models.IntegerField()
    #Linked to auto incremented ID of students table
    student_id = models.IntegerField()
    application_status_id = models.IntegerField()
    hiring_status_id = models.IntegerField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    personal_statement = models.CharField(max_length=400)
    class_grade = models.CharField(max_length=4, choices=DataDefinitions.GRADE_CHOICES)
    optional_fields = models.CharField(max_length=5000, validators=[validate_optional_field_json], default="")


class Professors(models.Model):
    ubit_name = models.CharField(max_length=10)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)

class StatusText(models.Model):
    # Status Types: 0 will be application status, 1 will be hiring status
    status_type = models.IntegerField()
    status_id = models.IntegerField()
    status_text = models.CharField(max_length=30)

class ApplicationFields(models.Model):
    field_name = models.CharField(max_length=30)
    field_text = models.CharField(max_length=30)
    is_default = models.BooleanField()
    from_student = models.BooleanField()
    data_type = models.CharField(max_length=6, choices=DataDefinitions.FIELD_TYPE_CHOICES)
    max_length = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(400)])


