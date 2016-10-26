from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Resume


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('document',)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()