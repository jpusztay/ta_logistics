from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from datetime import date
from ta_logistics_application.models import Courses, CourseApplicants, DataDefinitions, ApplicationFields
from ta_logistics_application.forms import StudentProfileForm, CreateCourseForm, OptionalFieldsForm, ApplicationForm


def index(request):
    template = loader.get_template('ta_logistics_application/index.html')
    return HttpResponse(template.render())


################ Student Context ################

def available_courses(request):
    current_course_list = Courses.objects.filter(is_active=True)
    context = {'current_course_list':current_course_list}
    template = loader.get_template('ta_logistics_application/professor/professor_index.html')
    return render(request, 'ta_logistics_application/professor/professor_index.html', context)


# Finish when student index is finished
# Get s_id and c_id parts working
def application(request):#, c_id, s_id):
    c_id = 6
    s_id = 1
    if request.method == 'POST':
        form = ApplicationForm(request.POST, course_id=c_id, student_id=s_id)
        if form.is_valid():
            form.save()
            template = loader.get_template('ta_logistics_application/student/submission_received.html')
            return HttpResponse(template.render())

    form = ApplicationForm(course_id=c_id, student_id=s_id)
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



################ Professor Context ################


def professor_index(request):
    p_id = 1
    current_course_list = Courses.objects.filter(professor_id=p_id, is_active=True)
    context = {'current_course_list':current_course_list}
    template = loader.get_template('ta_logistics_application/professor/professor_index.html')
    return render(request, 'ta_logistics_application/professor/professor_index.html', context)

def professor_course_applicants(request):
    data_defs = DataDefinitions()
    course_id = request.GET.urlencode().split('=')[-1]
    fields = []
    student_data = data_defs.getStudentDataForApplicantsView(fields=fields, course_id=course_id)
    #header_dict = data_defs.getAllFieldsDictionary()
    #field_text = [header_dict[x] for x in fields]
    course_applicant_data = {}

    #context = {
     #   'course_applicants': course_applicants,
     #   'field_names': field_names,
     #   'column_headers': field_text,
    #}
    #return render(request, 'ta_logistics_application/professor/professor_index.html', context)


def professor_create_course(request):
    if request.method == 'POST':
        selected_optionals = request.POST.getlist("select_optional_fields")
        # Hacky solution, possible rework in the future
        request.POST['selected_optional_field_ids'] = ','.join(map(str,selected_optionals))
        # Replace this with ID of professor that is signed in
        request.POST['professor_id'] = 1
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(professor_index)
        else:
            print(form.errors)
            return redirect(professor_index)

    context = {
        'form': CreateCourseForm(),
        'optional_fields': OptionalFieldsForm()
    }
    return render(request, 'ta_logistics_application/professor/create_course.html', context)
