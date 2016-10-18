from django import forms
from .models import Students, Classes, ApplicationFields, ClassApplicants, DataDefinitions


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
    class Meta:
        data_defs = DataDefinitions()
        model = ClassApplicants
        fields = ['class_id', 'student_id', 'application_status_id', 'hiring_status_id', 'optional_fields',
                  'personal_statement', 'class_grade']
        widgets = {
            'class_id': forms.HiddenInput(),
            'student_id': forms.HiddenInput(),
            'application_status_id': forms.HiddenInput(),
            'hiring_status_id': forms.HiddenInput(),
            'optional_fields': forms.HiddenInput(),
            'class_grade': forms.Select(choices=data_defs.GRADE_CHOICES, attrs={'placeholder': 'Select Grade You Recieved in Applying Class'}),
            'personal_statement': forms.Textarea(attrs={'placeholder': 'Enter a Brief Summary of Why You Want The Position'}),

        }
        labels = {

        }

    def __init__(self, *args, **kwargs):
        data_defs = DataDefinitions()
        self.class_id = kwargs.pop('class_id')
        self.student_id = kwargs.pop('student_id')
        self.application_status_id = 0
        self.hiring_status_id = 0
        optional_field_ids = map(int, Classes.objects.filter(id=self.class_id)['selected_optional_field_ids'].split())
        all_fields = ApplicationFields.objects.all()
        for f_id in optional_field_ids:
            field = ApplicationFields.objects.filter(id=f_id)
            data_type = field['data_type']
            if data_type == data_defs.INT_FIELD:
                self.fields[field['field_name']] = forms.NumberInput(label=field['field_text'])
            elif data_type == data_defs.FLOAT_FIELD:
                self.fields[field['field_name']] = forms.FloatField(label=field['field_text'])
            elif data_type == data_defs.TEXT_FIELD:
                self.fields[field['field_name']] = forms.TextInput(label=field['field_text'])
            elif data_type == data_defs.COMFORT_LVL_FIELD:
                self.fields[field['field_name']] = forms.ChoiceField(choices=data_defs.COMFORT_LVLS)
        super(ApplicationForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return True

    def save(self):
        return


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