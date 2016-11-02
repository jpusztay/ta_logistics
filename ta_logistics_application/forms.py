from django.contrib.auth.forms import AuthenticationForm
import json
from django import forms
from .models import Students, Classes, ApplicationFields, ClassApplicants, DataDefinitions

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))


class ResumeForm(forms.ModelForm):
    OPT_DATA_STR = 'optional_data'
################ Student Context ################
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['ubit_name', 'person_number', 'first_name', 'last_name', 'gpa', 'resume', 'teaching_experience']
        widgets = {
            'ubit_name': forms.TextInput(attrs={'placeholder': 'Enter UBIT Name'}),
            'person_number': forms.TextInput(attrs={'placeholder': 'Enter Person Number'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter Last Name'}),
            'teaching_experience': forms.Textarea(attrs={'placeholder': 'Enter a Brief Summary of Your Teaching Experience'}),
            'gpa': forms.Select(attrs={'placeholder': 'Select GPA'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class ApplicationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        data_defs = DataDefinitions()
        self.class_id = kwargs.pop('class_id')
        self.student_id = kwargs.pop('student_id')
        super(ApplicationForm, self).__init__(*args, **kwargs)

        self.application_status_id = 0
        self.hiring_status_id = 0
        self.field_text_list = {}
        # MAYBE LATER: Add student data fields as un-editable fields with student info
        #student = Students.objects.get(id=self.student_id)
        self.fields['class_grade'] = forms.ChoiceField(choices=data_defs.GRADE_CHOICES)
        self.fields['personal_statement'] = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter a Brief Summary of Why You Want The Position'}))
        self.optional_field_ids = map(int, Classes.objects.get(id=self.class_id).selected_optional_field_ids.split(","))
        for f_id in self.optional_field_ids:
            new_field = ApplicationFields.objects.get(id=f_id)
            data_type = new_field.data_type
            self.field_text_list[new_field.field_name] = data_type
            if data_type == data_defs.INT_FIELD:
                self.fields[new_field.field_name] = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': new_field.field_text}))
                self.fields[new_field.field_name].label = new_field.field_text
            elif data_type == data_defs.FLOAT_FIELD:
                self.fields[new_field.field_name] = forms.FloatField(label=new_field.field_text)
            elif data_type == data_defs.TEXT_FIELD:
                self.fields[new_field.field_name] = forms.TextInput(attrs={'placeholder': new_field.field_text})
                self.fields[new_field.field_name].label = new_field.field_text
            elif data_type == data_defs.COMFORT_LVL_FIELD:
                self.fields[new_field.field_name] = forms.ChoiceField(choices=data_defs.COMFORT_LVLS)
                self.fields[new_field.field_name].label = new_field.field_text
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def save(self):
        data = self.cleaned_data
        optional_data = {}
        optional_data[OPT_DATA_STR] = {}
        for key, value in self.field_text_list.items():
            optional_data[OPT_DATA_STR][key] = data[key]
        option_fields_json = json.dumps(optional_data)
        application = ClassApplicants(
            class_id=self.class_id,
            student_id=self.student_id,
            application_status_id=self.application_status_id,
            hiring_status_id=self.hiring_status_id,
            personal_statement=data['personal_statement'],
            class_grade=data['class_grade'],
            optional_fields=option_fields_json,
        )
        application.save()
        print("Save")


################ Professor Context ################

class CreateClassForm(forms.ModelForm):
    class Meta:
        data_defs = DataDefinitions()
        model = Classes
        fields = ['professor_id','class_listing_id', 'active_semester', 'class_name', 'available_hours',
                  'selected_optional_field_ids']
        widgets = {
            'professor_id': forms.HiddenInput(),
            'class_listing_id': forms.TextInput(attrs={'placeholder': 'e.g. CSE331'}),
            'active_semester': forms.Select(choices=data_defs.getActiveSemesters(), attrs={'placeholder': 'Select Active Semester'}),
            'class_name': forms.TextInput(attrs={'placeholder': 'e.g. Introduction to Algorithm Analysis and Design'}),
            'available_hours': forms.NumberInput(attrs={'placeholder': 'Estimate If You Don\'t Know Yet'}),
            'selected_optional_field_ids': forms.HiddenInput(),
        }
        labels = {
            'class_listing_id': 'Class ID',
            'active_semester': 'Active Semester',
            'class_name': 'Class Title',
            'available_hours': 'Hours Available in Budget',
        }


    def __init__(self, *args, **kwargs):
        super(CreateClassForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class OptionalFieldsForm(forms.Form):
    data_defs = DataDefinitions()
    select_optional_fields = forms.MultipleChoiceField(
        choices = data_defs.getOptionalFields(),
        widget  = forms.CheckboxSelectMultiple,
    )
    select_optional_fields.widget.attrs.update({
                'class': 'optional_field_check',
                'id': 'optional_field_check'
            })