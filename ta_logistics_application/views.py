from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader
from django.contrib.auth.decorators import login_required

from ta_logistics_application.forms import ResumeForm


def login(request):
    template = loader.get_template('ta_logistics_application/login.html')
    return HttpResponse(template.render())


@login_required(login_url='login/')
def group_index(request):
    if request.user.is_authenticated():
        if request.user.groups.all()[0].name == "faculty":
            template = loader.get_template('ta_logistics_application/professor/professor_index.html')
            return HttpResponse(template.render())
        elif request.user.groups.all()[0].name == "student":
            template = loader.get_template('ta_logistics_application/student/student_index.html')
            return HttpResponse(template.render())


@login_required(login_url='login/')
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


@login_required(login_url='login/')
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


@login_required(login_url='login/')
def student_profile(request):
    template = loader.get_template('ta_logistics_application/student/profile.html')
    return HttpResponse(template.render())