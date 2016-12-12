from django.db import models
from django.core.validators import validate_comma_separated_integer_list, MaxValueValidator, MinValueValidator
from ta_logistics_application.validators import validate_optional_field_json
from collections import OrderedDict
from django.conf import settings
import datetime, json


class DataDefinitions():
    BOOL_ACTIVE = (
        (1, 'Yes'),
        (0, 'Activate Later')
    )
    BOOL_YES_NO = (
        (True, 'Yes'),
        (False, 'No')
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

    NUM_CREDITS_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
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
        ('CMFT', 'Programming Language Comfort Level')
    )

    COMFORT_LVLS = (
        ('Expert','Expert'),
        ('Advanced','Advanced'),
        ('Moderate','Moderate'),
        ('Novice','Novice'),
        ('None','None'),
    )
    HIRING_STATUS = (
        (0, 'Pending Review'),
        (1, 'Rejected'),
        (2, 'Interviewing'),
        (3, 'Given Offer'),
        (4, 'Wait Listed'),
        (5, 'Accepted Offer'),
        (6, 'Declined Offer'),
    )
    APPLICATION_STATUS = (
        (0, 'Application Pending'),
        (1, 'Application Complete'),
        (2, 'Application Pending'),
        (3, 'Given Offer'),
        (4, 'Application Pending'),
        (5, 'Accepted Offer'),
        (6, 'Declined Offer'),
    )
    SPRING_FALL = (
        ('Spring', 'Spring'),
        ('Fall', 'Fall'),
        ('Both', 'Both'),

    )

    STUDENT_DATA_QUERY = "select * from ta_logistics_application_classapplicants AS applicants "+\
                         "JOIN ta_logistics_application_students as students on (applicants.student_id = students.id) "+\
                         "where applicants.class_id = %d"

    ALL_STUDENT_DATA_QUERY = "select * from ta_logistics_application_classapplicants AS applicants "+\
                             "JOIN ta_logistics_application_students as students on (applicants.student_id = students.id) "+\
                             "where applicants.hiring_status_id = %d"

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

    def getPayrollData(self):
        payroll_model_data = PayrollInfo.objects.filter(is_on_payroll=False)
        data = []
        for entry in payroll_model_data:
            payroll_data = OrderedDict()
            student_data = Students.objects.get(id=entry.student_id)
            class_data = Classes.objects.get(id=entry.class_id)
            professor_data = Professors.objects.get(id=class_data.professor_id)
            payroll_data['class_listing_id'] = class_data.class_listing_id
            payroll_data['professor_data'] = professor_data.first_name + " " + professor_data.last_name + " (" + professor_data.ubit_name + ")"
            payroll_data['student_data'] = student_data.first_name + " " + student_data.last_name + " (" + student_data.ubit_name + ")"
            payroll_data['student_person_number'] = student_data.person_number

            payroll_data['fall_spring_or_both'] = entry.fall_and_spring
            payroll_data['has_social_security_number'] = entry.has_ssn
            payroll_data['been_cse_ta'] = entry.been_student_assistant
            payroll_data['ever_been_on_ub_payroll'] = entry.been_on_ub_payroll
            payroll_data['working_on_campus_while_being_ta'] = entry.working_on_campus_while_being_ta
            payroll_data['id'] = entry.id

            data.append(payroll_data)
        return data


    def getStudentAppliedClasses(self, student_id):
        applications = ClassApplicants.objects.filter(student_id=student_id)
        data = []
        for application in applications:
            app_data = OrderedDict()
            curr_class = Classes.objects.get(id=application.class_id)
            app_data['class_id'] = curr_class.class_listing_id
            app_data['id'] = curr_class.id
            app_data['hiring_status_id'] = application.hiring_status_id
            for choice_tuple in self.APPLICATION_STATUS:
                choice_id, choice_name = choice_tuple
                if choice_id == application.hiring_status_id:
                    app_data['application_status'] = choice_name
                    break
            data.append(app_data)
        return data


    def getStudentDataForApplicantsView(self, class_id):
        applicants = ClassApplicants.objects.filter(class_id=class_id).select_related()
        main_data_fields = ['ubit_name', 'first_name', 'last_name', 'hiring_status', 'class_grade', 'gpa',]
        secondary_data_fields = ['personal_statement', 'resume']
        raw_applicant_data = ClassApplicants.objects.raw(self.STUDENT_DATA_QUERY%class_id)
        main_student_data = []
        secondary_student_data = []
        optional_field_ids = list(map(int, Classes.objects.get(id=class_id).selected_optional_field_ids.split(',')))
        for applicant in raw_applicant_data:
            main_student_data.append(OrderedDict())
            secondary_student_data = OrderedDict()
            for field in main_data_fields:
                if field == 'hiring_status':
                    for tup in self.HIRING_STATUS:
                        id, name = tup
                        if id == applicant.hiring_status_id:
                            main_student_data[-1][field] = name
                            break
                else:
                    main_student_data[-1][field] = getattr(applicant, field)
            optional_field_data = json.loads(applicant.optional_fields)
            for ident in optional_field_ids:
                opt_field = ApplicationFields.objects.get(id=ident).field_name
                main_student_data[-1][opt_field] = optional_field_data[self.OPTIONAL_DATA][opt_field]
            for field in secondary_data_fields:
                if field == 'resume':
                    secondary_student_data[field] = getattr(applicant, field)
                else:
                    secondary_student_data[field] = getattr(applicant, field)
            main_student_data[-1]['secondary_student_data'] = secondary_student_data

        return main_student_data

    def getStudentDataForRegistration(self):
        raw_data = ClassApplicants.objects.raw(self.ALL_STUDENT_DATA_QUERY%5)
        unreg_hires = []
        fields = ['ubit_name', 'first_name', 'last_name', 'class_id', 'number_credits', 'is_registered_for_credit']
        for student in raw_data:
            unreg_hires.append(OrderedDict())
            if student.hiring_status_id == 5 and student.is_registered_for_credit == 0:
                for field in fields:
                    if field == 'hiring_status':
                        for tup in self.HIRING_STATUS:
                            id, name = tup
                            if id == student.hiring_status_id:
                                unreg_hires[-1][field] = name
                                break
                    else:
                        unreg_hires[-1][field] = getattr(student, field)
        return unreg_hires


class Students(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    ubit_name = models.CharField(max_length=10, unique=True)
    person_number = models.CharField(max_length=8, unique=True)
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
    # Linked to auto incremented ID of classes table
    class_id = models.IntegerField()
    # Linked to auto incremented ID of students table
    student_id = models.IntegerField()
    hiring_status_id = models.IntegerField(choices=DataDefinitions.HIRING_STATUS, default=0)
    date_submitted = models.DateTimeField(auto_now_add=True)
    personal_statement = models.CharField(max_length=400)
    class_grade = models.CharField(max_length=4, choices=DataDefinitions.GRADE_CHOICES)
    optional_fields = models.CharField(max_length=5000, validators=[validate_optional_field_json], default="")
    number_credits = models.IntegerField(choices=DataDefinitions.NUM_CREDITS_CHOICES, default=0)
    is_registered_for_credit = models.BooleanField(default=False)


class Professors(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    ubit_name = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)


class ApplicationFields(models.Model):
    field_name = models.CharField(max_length=30)
    field_text = models.CharField(max_length=30)
    is_default = models.BooleanField(default=0)
    from_student = models.BooleanField(default=0)
    data_type = models.CharField(max_length=6, choices=DataDefinitions.FIELD_TYPE_CHOICES)
    max_length = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(400)], default=0)
    select_options = models.CharField(max_length=500, default="")


class PayrollInfo(models.Model):
    student_id = models.IntegerField()
    class_id = models.IntegerField()
    has_ssn = models.BooleanField(default=False, choices=DataDefinitions.BOOL_YES_NO)
    been_on_ub_payroll = models.BooleanField(default=False, choices=DataDefinitions.BOOL_YES_NO)
    been_student_assistant = models.BooleanField(default=False, choices=DataDefinitions.BOOL_YES_NO)
    working_on_campus_while_being_ta = models.BooleanField(default=False, choices=DataDefinitions.BOOL_YES_NO)
    fall_and_spring = models.TextField(default=False, choices=DataDefinitions.SPRING_FALL)
    is_on_payroll = models.BooleanField(default=False)