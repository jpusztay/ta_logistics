from django.db import models
from django.core.validators import validate_comma_separated_integer_list, MaxValueValidator, MinValueValidator
from ta_logistics_application.validators import validate_optional_field_json
from collections import OrderedDict
import datetime, json

class DataDefinitions():
    BOOL_YES_NO = (
        (1, 'Yes'),
        (0, 'Activate Later')
    )
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
        ('A','A'),
        ('A-','A-'),
        ('B+','B+'),
        ('B','B'),
        ('B-','B-'),
        ('C+','C+'),
        ('C','C'),
        ('C-','C-'),
        ('< C-','< C-'),
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
    APPLICATION_STATUS = (
        (0, 'Application Submitted'),
        (1, 'Application Pending'),
        (2, 'Application Complete'),
    )
    HIRING_STATUS = (
        (0, 'Pending Review'),
        (1, 'Rejected'),
        (2, 'Interviewing'),
        (3, 'Accepted'),
        (4, 'Wait Listed'),
    )

    STUDENT_DATA_QUERY = "select * from ta_logistics_application_classapplicants AS applicants "+\
                         "JOIN ta_logistics_application_students as students on (applicants.student_id = students.id) "+\
                         "where applicants.class_id = %d"

    INT_FIELD = "INT"
    FLOAT_FIELD = "FLOAT"
    TEXT_FIELD = "TEXT"
    COMFORT_LVL_FIELD = "CMFT"
    OPTIONAL_DATA = "optional_data"

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

    def getStudentDataForApplicantsView(self, class_id):
        applicants = ClassApplicants.objects.filter(class_id=class_id).select_related()
        main_data_fields = ['ubit_name', 'first_name', 'last_name', 'hiring_status', 'class_grade', 'gpa',]
        secondary_data_fields = ['personal_statement', 'resume']
        raw_applicant_data = ClassApplicants.objects.raw(self.STUDENT_DATA_QUERY%class_id)
        main_student_data = []
        secondary_student_data = []
        optional_field_ids = list(map(int, Classes.objects.get(id=class_id).selected_optional_field_ids.split(',')))
        for applicant in raw_applicant_data:
            index = len(main_student_data)
            main_student_data.append(OrderedDict())
            secondary_student_data.append(OrderedDict())
            for field in main_data_fields:
                if field == 'hiring_status':
                    for tup in self.HIRING_STATUS:
                        id, name = tup
                        if id == applicant.hiring_status_id:
                            main_student_data[index][field] = name
                            break
                else:
                    main_student_data[index][field] = getattr(applicant, field)
            optional_field_data = json.loads(applicant.optional_fields)
            print(optional_field_ids)
            for ident in optional_field_ids:
                print("Should be 9")
                opt_field = ApplicationFields.objects.get(id=ident).field_name
                main_student_data[index][opt_field] = optional_field_data[self.OPTIONAL_DATA][opt_field]
            for field in secondary_data_fields:
                secondary_student_data[index][field] = getattr(applicant, field)
        print(main_student_data)
        return main_student_data, secondary_student_data


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
    is_active = models.BooleanField(default=False)
    selected_optional_field_ids = models.CharField(max_length = 200, validators=[validate_comma_separated_integer_list], null=True)

class ClassApplicants(models.Model):
    #Linked to auto incremented ID of classes table
    class_id = models.IntegerField()
    #Linked to auto incremented ID of students table
    student_id = models.IntegerField()
    application_status_id = models.IntegerField(choices=DataDefinitions.APPLICATION_STATUS, default=0)
    hiring_status_id = models.IntegerField(choices=DataDefinitions.HIRING_STATUS, default=0)
    date_submitted = models.DateTimeField(auto_now_add=True)
    personal_statement = models.CharField(max_length=400)
    class_grade = models.CharField(max_length=4, choices=DataDefinitions.GRADE_CHOICES)
    optional_fields = models.CharField(max_length=5000, validators=[validate_optional_field_json], default="")


class Professors(models.Model):
    ubit_name = models.CharField(max_length=10)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)


class ApplicationFields(models.Model):
    field_name = models.CharField(max_length=30)
    field_text = models.CharField(max_length=30)
    is_default = models.BooleanField()
    from_student = models.BooleanField()
    data_type = models.CharField(max_length=6, choices=DataDefinitions.FIELD_TYPE_CHOICES)
    max_length = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(400)])

