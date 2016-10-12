from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader

from ta_logistics_application.forms import ResumeForm

def index(request):
    template = loader.get_template('ta_logistics_application/index.html')
    return HttpResponse(template.render())

def submit(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            template = loader.get_template('ta_logistics_application/student/submission_received.html')
            return HttpResponse(template.render())
    else:
        form = ResumeForm()
    return render(request, 'ta_logistics_application/student/application.html', {'form': form})

def edit_student_profile(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            template = loader.get_template('ta_logistics_application/student/edit_profile.html')
            return HttpResponse(template.render())
    else:
        form = ResumeForm()
    return render(request, 'ta_logistics_application/student/edit_profile.html', {'form': form})

def student_profile(request):
    template = loader.get_template('ta_logistics_application/student/profile.html')
    return HttpResponse(template.render())

def create_student_account(request):
    template = loader.get_template('ta_logistics_application/student/create_account.html')
    return HttpResponse(template.render())