from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from ta_logistics_application.models import Classes, ApplicationFields, DataDefinitions
from ta_logistics_application.forms import StudentProfileForm, CreateClassForm, OptionalFieldsForm, ApplicationForm


def login(request):
    template = loader.get_template('ta_logistics_application/login.html')
    return HttpResponse(template.render())


@login_required(login_url='login')
def group_index(request):
    if request.user.is_authenticated():
        if request.user.groups.all()[0].name == "faculty":
            template = loader.get_template('ta_logistics_application/professor/professor_index.html')
            return HttpResponse(template.render())
        elif request.user.groups.all()[0].name == "student":
            template = loader.get_template('ta_logistics_application/student/student_index.html')
            return HttpResponse(template.render())


################ Student Context ################
# Finish when student index is finished
# Get s_id and c_id parts working
def application(request):#, c_id, s_id):
    c_id = 6
    s_id = 1
    if request.method == 'POST':
        form = ApplicationForm(request.POST, class_id=c_id, student_id=s_id)
        if form.is_valid():
            form.save()
            template = loader.get_template('ta_logistics_application/student/submission_received.html')
            return HttpResponse(template.render())

    form = ApplicationForm(class_id=c_id, student_id=s_id)
    return render(request, 'ta_logistics_application/student/application.html', {'form': form})


@login_required(login_url='login')
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


@login_required(login_url='login')
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



################ Professor Context ################


def professor_index(request):
    p_id = 1
    current_class_list = Classes.objects.filter(professor_id=p_id, is_active=True)
    context = {'current_class_list':current_class_list}
    template = loader.get_template('ta_logistics_application/professor/professor_index.html')
    return render(request, 'ta_logistics_application/professor/professor_index.html', context)


def professor_create_class(request):
    if request.method == 'POST':
        selected_optionals = request.POST.getlist("select_optional_fields")
        # Hacky solution, possible rework in the future
        request.POST['selected_optional_field_ids'] = ','.join(map(str,selected_optionals))
        # Replace this with ID of professor that is signed in
        request.POST['professor_id'] = 1
        form = CreateClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(professor_index)
        else:
            print(form.errors)
            return redirect(professor_index)

    context = {
        'form': CreateClassForm(),
        'optional_fields': OptionalFieldsForm()
    }
    return render(request, 'ta_logistics_application/professor/create_class.html', context)

def professor_class_applicants(request):
    data_defs = DataDefinitions()
    class_id = int(request.GET.urlencode().split('=')[-1])
    main_student_data, secondary_student_data = data_defs.getStudentDataForApplicantsView(class_id=class_id)


    context = {
        'main_student_data': main_student_data,
        'secondary_student_data': secondary_student_data,
    }

    return render(request, 'ta_logistics_application/professor/professor_class_applicants.html', context)