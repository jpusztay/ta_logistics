from django.contrib.auth.forms import AuthenticationForm
import json
from django import forms
from .models import Students, Classes, ClassApplicants, DataDefinitions, ApplicationFields
from registration.forms import RegistrationForm


#String Constants go HERE:
OPT_DATA_STR = 'optional_data'


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))



################ Student Context ################
class ClassListForm(forms.Form):
    """
    This form will simply show a dropdown of available classes.
    """

    class_list = forms.ModelChoiceField(queryset=Classes.objects.values())



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

        self.hiring_status_id = 0
        self.field_text_list = {}
        # MAYBE LATER: Add student data fields as un-editable fields with student info
        #student = Students.objects.get(id=self.student_id)
        self.fields['class_grade'] = forms.ChoiceField(choices=data_defs.GRADE_CHOICES)
        self.fields['number_credits'] = forms.ChoiceField(choices=data_defs.NUM_CREDITS_CHOICES)
        self.fields['number_credits'].label = "Select number of 495 credits (0-4)"
        self.fields['personal_statement'] = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter a Brief Summary of Why You Want The Position'}))
        self.optional_field_ids = map(int, Classes.objects.get(id=self.class_id).selected_optional_field_ids.split(","))
        for f_id in self.optional_field_ids:
            new_field = ApplicationFields.objects.get(id=f_id)
            data_type = new_field.data_type
            self.field_text_list[new_field.field_name] = data_type
            if data_type == data_defs.INT_FIELD:
                if new_field.select_options != '':
                    choice_list = new_field.select_options.split(',')
                    choices = ()
                    for item in choice_list:
                        choices = choices + ((item, item),)
                    self.fields[new_field.field_name] = forms.ChoiceField(choices=choices)
                else:
                    self.fields[new_field.field_name] = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': new_field.field_text}))
                self.fields[new_field.field_name].label = new_field.field_text
            elif data_type == data_defs.FLOAT_FIELD:
                if new_field.select_options != '':
                    choice_list = new_field.select_options.split(',')
                    choices = ()
                    for item in choice_list:
                        choices = choices + ((item, item),)
                    self.fields[new_field.field_name] = forms.ChoiceField(choices=choices)
                else:
                    self.fields[new_field.field_name] = forms.FloatField(label=new_field.field_text)
            elif data_type == data_defs.TEXT_FIELD:
                if new_field.select_options != '':
                    choice_list = new_field.select_options.split(',')
                    choices = ()
                    for item in choice_list:
                        choices = choices + ((item, item),)
                    self.fields[new_field.field_name] = forms.ChoiceField(choices=choices)
                else:
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
            hiring_status_id=self.hiring_status_id,
            personal_statement=data['personal_statement'],
            class_grade=data['class_grade'],
            optional_fields=option_fields_json,
            number_credits=data['number_credits']
        )
        application.save()


################ Professor Context ################

class CreateClassForm(forms.ModelForm):
    class Meta:
        data_defs = DataDefinitions()
        model = Classes
        fields = ['professor_id','class_listing_id', 'active_semester', 'is_active', 'class_name', 'available_hours',
                  'selected_optional_field_ids']
        widgets = {
            'professor_id': forms.HiddenInput(),
            'class_listing_id': forms.TextInput(attrs={'placeholder': 'e.g. CSE331'}),
            'active_semester': forms.Select(choices=data_defs.getActiveSemesters(), attrs={'placeholder': 'Select Active Semester'}),
            'is_active': forms.Select(choices=data_defs.BOOL_ACTIVE),
            'class_name': forms.TextInput(attrs={'placeholder': 'e.g. Introduction to Algorithm Analysis and Design'}),
            'available_hours': forms.NumberInput(attrs={'placeholder': 'Estimate If You Don\'t Know Yet'}),
            'selected_optional_field_ids': forms.HiddenInput(),
        }
        labels = {
            'class_listing_id': 'Class ID',
            'active_semester': 'Active Semester',
            'is_active': "Activate This Class Upon Creation?",
            'class_name': 'Class Title',
            'available_hours': 'Hours Available in Budget (Total for Semester)',
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
        widget = forms.CheckboxSelectMultiple,
    )
    select_optional_fields.widget.attrs.update({
                'class': 'optional_field_check',
                'id': 'optional_field_check'
            })
    def __init__(self, *args, **kwargs):
        super(OptionalFieldsForm, self).__init__(*args, **kwargs)


class AddOptionalFieldForm(forms.ModelForm):
    class Meta:
        data_defs = DataDefinitions()
        model = ApplicationFields
        fields = ['field_name', 'field_text', 'data_type', 'select_options', 'max_length']

        widgets = {
            'field_name': forms.HiddenInput(),
            'field_text': forms.TextInput(attrs={'placeholder': 'e.g. C++ Comfort Level'}),
            'data_type': forms.Select(choices=data_defs.FIELD_TYPE_CHOICES),
            'max_length': forms.NumberInput(attrs={'placeholder': 'Integer between 1 and 400', 'initial': ''}, ),
            'select_options': forms.Textarea(attrs={'placeholder': 'Enter values for students to select from. Put one on each line. For example:\nBad\nNeutral\nGood', 'required': False},),
        }
        labels = {
            'field_text': 'Field Title',
            'data_type': 'Data Type',
            'select_options': 'Select Options',
            'max_length': 'Max Length/Size',
        }

    def __init__(self, *args, **kwargs):
        super(AddOptionalFieldForm, self).__init__(*args, **kwargs)
        self.fields['select_options'].required = False
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class CustomRegForm(RegistrationForm):
    pass