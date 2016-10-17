from django import forms
from datetime import datetime
from .models import Students, Classes, ApplicationFields

"""
Generates Active semester tuples (e.g. ('FA16', 'Fall 2016'))
for create class 'active semester' field
"""
def getActiveSemesters():
    ret = []
    curYear = datetime.now().year
    for i in range(curYear, curYear + 3):
        ret.append(('FA' + str(i)[-2:], 'Fall ' + str(i)))
        ret.append(('SP' + str(i)[-2:], 'Spring ' + str(i)))
    return tuple(ret)

def getOptionalFields():
    ret = []
    for i in ApplicationFields.objects.filter(is_default=False):
        ret.append((i.id, i.field_text))
    return tuple(ret)

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

class CreateClassForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = ['class_listing_id', 'active_semester', 'class_name', 'available_hours']
        widgets = {
            'class_listing_id': forms.TextInput(attrs={'placeholder': 'e.g. CSE331'}),
            'active_semester': forms.Select(choices=getActiveSemesters()),
            'class_name': forms.TextInput(attrs={'placeholder': 'e.g. Introduction to Algorithm Analysis and Design'}),
            'available_hours': forms.TextInput(attrs={'placeholder': 'Estimate If You Don\'t Know Yet'}),
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
    select_optional_fields = forms.MultipleChoiceField(
        choices = getOptionalFields(),
        widget  = forms.CheckboxSelectMultiple,
    )
    select_optional_fields.widget.attrs.update({
                'class': 'optional_field_check',
                'id': 'optional_field_check'
            })