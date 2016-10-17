from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader
from ta_logistics_application.models import Classes, ApplicationFields
from ta_logistics_application.forms import StudentProfileForm, CreateClassForm, OptionalFieldsForm

def index(request):
    template = loader.get_template('ta_logistics_application/index.html')
    return HttpResponse(template.render())

def submit(request):
    if request.method == 'POST':
        print(request.POST)
        """form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            template = loader.get_template('ta_logistics_application/student/submission_received.html')
            return HttpResponse(template.render())"""
    else:
        form = StudentProfileForm()
    return render(request, 'ta_logistics_application/student/application.html', {'form': form})

def edit_student_profile(request):
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            template = loader.get_template('ta_logistics_application/student/edit_profile.html')
            return HttpResponse(template.render())
    else:
        form = StudentProfileForm()
    return render(request, 'ta_logistics_application/student/edit_profile.html', {'form': form})

def student_profile(request):
    template = loader.get_template('ta_logistics_application/student/profile.html')
    return HttpResponse(template.render())

def create_student_account(request):
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            template = loader.get_template('ta_logistics_application/student/submission_received.html')
            return HttpResponse(template.render())
    else:
        form = StudentProfileForm()
    return render(request, 'ta_logistics_application/student/create_account.html', {'form': form})

def professor_index(request):
    p_id = 1
    current_class_list = Classes.objects.filter(professor_id=p_id, active_semester='FA16')
    context = {'current_class_list':current_class_list}
    template = loader.get_template('ta_logistics_application/professor/professor_index.html')
    return render(request, 'ta_logistics_application/professor/professor_index.html', context)

def professor_create_class(request):
    if request.method == 'POST':
        selected_optionals = request.POST.getlist("select_optional_fields")
        #print("Selected: ")
        print(selected_optionals)

    context = {
        'form': CreateClassForm(),
        'optional_fields': OptionalFieldsForm()
    }
    return render(request, 'ta_logistics_application/professor/create_class.html', context)
